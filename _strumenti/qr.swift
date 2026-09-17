// Genera un codice QR in SVG e controlla che si legga.
// Uso:  swift _strumenti/qr.swift URL assets/qr/NOME.svg
//
// Il codice è creato con il generatore di macOS (Core Image, correzione M),
// scritto in SVG con margine bianco di 4 moduli, poi ridisegnato in grande
// e riletto con il lettore QR di macOS: se il testo letto non è identico
// all'indirizzo, lo script si ferma con errore.
import CoreImage
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { fputs("uso: swift qr.swift URL OUT.svg\n", stderr); exit(2) }
let text = args[1], outPath = args[2]

let filter = CIFilter(name: "CIQRCodeGenerator")!
filter.setValue(text.data(using: .utf8)!, forKey: "inputMessage")
filter.setValue("M", forKey: "inputCorrectionLevel")
let ci = filter.outputImage!
let ctx = CIContext()
let w = Int(ci.extent.width), h = Int(ci.extent.height)
guard let cg = ctx.createCGImage(ci, from: ci.extent) else { exit(1) }

// pixel → moduli (1 pixel = 1 modulo)
var px = [UInt8](repeating: 0, count: w * h * 4)
let space = CGColorSpaceCreateDeviceRGB()
let bctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
                     space: space, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
bctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
var dark = [[Bool]](repeating: [Bool](repeating: false, count: w), count: h)
var minX = w, minY = h, maxX = -1, maxY = -1
for y in 0..<h { for x in 0..<w {
  let on = px[(y * w + x) * 4] < 128
  dark[y][x] = on
  if on { minX = min(minX, x); maxX = max(maxX, x); minY = min(minY, y); maxY = max(maxY, y) }
} }
let n = maxX - minX + 1, q = 4, size = n + 2 * q

var path = ""
for y in 0..<n {
  var x = 0
  while x < n {
    if dark[minY + y][minX + x] {
      var run = 1
      while x + run < n && dark[minY + y][minX + x + run] { run += 1 }
      path += "M\(x + q) \(y + q)h\(run)v1h-\(run)z"
      x += run
    } else { x += 1 }
  }
}
let svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 \(size) \(size)" shape-rendering="crispEdges"><rect width="\(size)" height="\(size)" fill="#fff"/><path fill="#000a49" d="\(path)"/></svg>

"""

// verifica: disegno a 12 px per modulo e rilettura
let scale = 12, big = size * scale
let vctx = CGContext(data: nil, width: big, height: big, bitsPerComponent: 8, bytesPerRow: 0,
                     space: space, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
vctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1)); vctx.fill(CGRect(x: 0, y: 0, width: big, height: big))
vctx.setFillColor(CGColor(red: 0, green: 10.0 / 255, blue: 73.0 / 255, alpha: 1))
for y in 0..<n { for x in 0..<n where dark[minY + y][minX + x] {
  vctx.fill(CGRect(x: (x + q) * scale, y: big - (y + q + 1) * scale, width: scale, height: scale))
} }
let detector = CIDetector(ofType: CIDetectorTypeQRCode, context: nil, options: [CIDetectorAccuracy: CIDetectorAccuracyHigh])!
let found = detector.features(in: CIImage(cgImage: vctx.makeImage()!)).compactMap { ($0 as? CIQRCodeFeature)?.messageString }
guard found == [text] else { fputs("ERRORE: letto \(found) invece di \(text)\n", stderr); exit(1) }

try! svg.write(toFile: outPath, atomically: true, encoding: .utf8)
print("ok \(outPath) · \(n) moduli · letto: \(found[0])")
