# Pulse Counter (Saleae Logic 2)

Live running count of rising edges on one digital channel, shown as bubbles on the timeline and rows in the Data Table while the capture runs. Designed for rates up to about 5 kHz.

## Install
1. In Logic 2 open the Extensions panel (right-hand sidebar).
2. Click the three-dot menu, then **Load Existing Extension**, and pick `extension.json` in this folder.

## Set up
1. Set the digital sample rate to at least 1 MS/s.
2. Add the **Simple Parallel** analyser:
   - Clock: the pulse channel, rising edge.
   - D0: the same channel. If Logic rejects the duplicate, use any spare channel. D1 onwards: none.
3. Add the **Pulse Counter** analyser and set its input to the Simple Parallel analyser.
4. Set **gate_ms** (bubble update interval). Left blank it defaults to 100 ms.
5. Start the capture. Each bubble spans one gate window and shows the total count since the capture began.

Optionally hide the Simple Parallel analyser's own bubbles (eye icon) to keep the timeline readable.

## Behaviour
- No pulses means no new bubbles. The final partial window is shown when the next edge arrives.
- The total resets at the start of each capture.
