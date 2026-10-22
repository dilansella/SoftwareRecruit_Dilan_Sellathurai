#= Socket Communication

`rover.py` streams `Utah.bmp` to `basestation.py` over TCP on localhost
(127.0.0.1, port 5555)
\
`output.bmp` is written by the base station. To verify the transfer, compare
it with the original: `fc /b Utah.bmp output.bmp` They should be identical.

Why TCP
The task is to send an image, so the output must match the input .
TCP delivers bytes reliably and in the order theyre supposed to be in, so a damaged never
corrupts the bitmap. UDP would need me to add my own chunk numbering,
reordering, and retransmission to get the same get the same thign that TCP already has buolt in.

For live video (which isnt the task), UDP is usualy the better choice. A late frame is not good, and
retransmitting an old frame delays the newer ones .


Message format
Every frame is a 4 byte big-endian length followed by the image bytes.
A length of 0 marks the end of the stream.

TCP is a continuous byte stream with no message boundaries, so the receiver
needs the length to know where one frame ends and the next begins.

Streaming
The task says to design it "as" if streaming video, so the rover sends the
image 3 times as separate frames (`FRAMES` in `rover.py`), then the end
marker. The base station overwrites `output.bmp` with each valid frame

Validation
The base station only saves a frame if it starts with the `BM` signature and
the bits-per-pixel field (byte 28 of the header, little-endian) equals 24.
Anything else is dropped, as a live viewer would skip a bad frame.

 Error handling 
-Timeouts (5 s on the rover, 10 s on the base station) prevent hanging
  forever if the other side stalls.
-The rover prints a clear message if `Utah.bmp` is missing or the base
  station isn't running.
-The base station reports a dropped connection instead of crashing.
-`SO_REUSEADDR` lets the base station restart immediately without an
  "address already in use" error.

Image size and quality
I didnt reduce the image. its sent byte for byte, so the output is an
exact .


Integrity checks
I didn't add my own checksum because TCP already checksums segments and
retransmits damaged ones. A checksum would only matter over UDP, or to catch
bugs in my own framing code.

 Limitations
-The base station accepts one rover connection at a time and exits after the
  stream ends.
 No encryption or authentication, so anyone who can reach port 5555 could
  send frames.
-he whole image is loaded into memory before sending, which is fine for one
  bitmap but wouldn't suit a continuous camera feed.