// Converte un video per il sito: H.264 a circa 2 Mbps, lato lungo 1280 px, AAC 128 kbps,
// MP4 ottimizzato per il web, taglio opzionale e dissolvenza dell'audio in chiusura.
// Crea anche l'immagine di copertina (stesso nome, .jpg).
//
// Uso: swift _strumenti/video.swift INGRESSO.mp4 USCITA.mp4 INIZIO FINE COPERTINA_SEC
//      (FINE = 0 significa fino alla fine del video; secondi con il punto decimale)
import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count == 6 else { print("uso: INGRESSO USCITA INIZIO FINE COPERTINA_SEC"); exit(1) }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])
let startSec = Double(args[3]) ?? 0
let endArg = Double(args[4]) ?? 0
let posterSec = Double(args[5]) ?? 1
let videoBitrate = 2_200_000
let longSide: CGFloat = 1280

func fail(_ msg: String) -> Never { print("errore:", msg); exit(1) }

let asset = AVURLAsset(url: input)
let sem = DispatchSemaphore(value: 0)

Task {
    do {
        let duration = try await asset.load(.duration).seconds
        let endSec = endArg > 0 ? min(endArg, duration) : duration
        let range = CMTimeRange(start: CMTime(seconds: startSec, preferredTimescale: 600),
                                end: CMTime(seconds: endSec, preferredTimescale: 600))
        guard let vTrack = try await asset.loadTracks(withMediaType: .video).first else { fail("nessuna traccia video") }
        let aTrack = try await asset.loadTracks(withMediaType: .audio).first
        let natural = try await vTrack.load(.naturalSize)
        let transform = try await vTrack.load(.preferredTransform)
        let fps = try await vTrack.load(.nominalFrameRate)

        // dimensioni di codifica (prima della rotazione), lato lungo 1280, pari
        let scale = min(1, longSide / max(natural.width, natural.height))
        let w = Int((natural.width * scale / 2).rounded()) * 2
        let h = Int((natural.height * scale / 2).rounded()) * 2

        try? FileManager.default.removeItem(at: output)
        let reader = try AVAssetReader(asset: asset)
        reader.timeRange = range
        let writer = try AVAssetWriter(outputURL: output, fileType: .mp4)
        writer.shouldOptimizeForNetworkUse = true

        let vOut = AVAssetReaderTrackOutput(track: vTrack, outputSettings: [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange
        ])
        vOut.alwaysCopiesSampleData = false
        reader.add(vOut)
        let vIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: w,
            AVVideoHeightKey: h,
            AVVideoScalingModeKey: AVVideoScalingModeResizeAspectFill,
            AVVideoCompressionPropertiesKey: [
                AVVideoAverageBitRateKey: videoBitrate,
                AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
                AVVideoMaxKeyFrameIntervalKey: Int(max(fps, 24)) * 2,
                AVVideoExpectedSourceFrameRateKey: Int(max(fps, 24))
            ]
        ])
        vIn.transform = transform
        vIn.expectsMediaDataInRealTime = false
        writer.add(vIn)

        var aOut: AVAssetReaderAudioMixOutput?
        var aIn: AVAssetWriterInput?
        if let aTrack = aTrack {
            let mixOut = AVAssetReaderAudioMixOutput(audioTracks: [aTrack], audioSettings: [
                AVFormatIDKey: kAudioFormatLinearPCM, AVLinearPCMBitDepthKey: 16,
                AVLinearPCMIsFloatKey: false, AVLinearPCMIsBigEndianKey: false, AVLinearPCMIsNonInterleaved: false
            ])
            let params = AVMutableAudioMixInputParameters(track: aTrack)
            if startSec > 0 {
                params.setVolumeRamp(fromStartVolume: 0, toEndVolume: 1,
                                     timeRange: CMTimeRange(start: range.start, duration: CMTime(seconds: 0.3, preferredTimescale: 600)))
            }
            let fade = min(1.0, (endSec - startSec) / 4)
            params.setVolumeRamp(fromStartVolume: 1, toEndVolume: 0,
                                 timeRange: CMTimeRange(start: CMTime(seconds: endSec - fade, preferredTimescale: 600),
                                                        duration: CMTime(seconds: fade, preferredTimescale: 600)))
            let mix = AVMutableAudioMix(); mix.inputParameters = [params]
            mixOut.audioMix = mix
            reader.add(mixOut)
            let input = AVAssetWriterInput(mediaType: .audio, outputSettings: [
                AVFormatIDKey: kAudioFormatMPEG4AAC, AVNumberOfChannelsKey: 2,
                AVSampleRateKey: 44100, AVEncoderBitRateKey: 128_000
            ])
            input.expectsMediaDataInRealTime = false
            writer.add(input)
            aOut = mixOut; aIn = input
        }

        guard reader.startReading() else { fail(reader.error?.localizedDescription ?? "lettura") }
        guard writer.startWriting() else { fail(writer.error?.localizedDescription ?? "scrittura") }
        writer.startSession(atSourceTime: range.start)

        let group = DispatchGroup()
        func pump(_ out: AVAssetReaderOutput, _ inp: AVAssetWriterInput, _ label: String) {
            group.enter()
            inp.requestMediaDataWhenReady(on: DispatchQueue(label: label)) {
                while inp.isReadyForMoreMediaData {
                    if let buf = out.copyNextSampleBuffer() {
                        if !inp.append(buf) { inp.markAsFinished(); group.leave(); return }
                    } else {
                        inp.markAsFinished(); group.leave(); return
                    }
                }
            }
        }
        pump(vOut, vIn, "video")
        if let aOut = aOut, let aIn = aIn { pump(aOut, aIn, "audio") }
        group.wait()
        await writer.finishWriting()
        if writer.status != .completed { fail(writer.error?.localizedDescription ?? "chiusura file") }

        // copertina
        let gen = AVAssetImageGenerator(asset: asset)
        gen.appliesPreferredTrackTransform = true
        gen.maximumSize = CGSize(width: longSide, height: longSide)
        gen.requestedTimeToleranceBefore = .zero
        gen.requestedTimeToleranceAfter = .zero
        let cg = try gen.copyCGImage(at: CMTime(seconds: posterSec, preferredTimescale: 600), actualTime: nil)
        let jpg = NSBitmapImageRep(cgImage: cg).representation(using: .jpeg, properties: [.compressionFactor: 0.78])
        try jpg?.write(to: output.deletingPathExtension().appendingPathExtension("jpg"))

        let size = (try? FileManager.default.attributesOfItem(atPath: output.path)[.size] as? Int) ?? 0
        print("ok", output.lastPathComponent, String(format: "%.1f s", endSec - startSec), "\(size / 1024) KB", "copertina \(cg.width)x\(cg.height)")
    } catch {
        fail(error.localizedDescription)
    }
    sem.signal()
}
sem.wait()
