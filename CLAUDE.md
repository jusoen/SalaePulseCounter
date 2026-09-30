# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is
A Saleae Logic 2 High Level Analyser (HLA) extension that shows a live running count of rising edges on one digital channel (target rate up to about 5 kHz). There is no build, lint or test tooling. The code only runs inside the Logic 2 app, which supplies the `saleae.analyzers` module, so it cannot be executed or unit-tested on the host.

## Architecture
- `extension.json` is the manifest Logic 2 loads. `entryPoint` is `module.Class` (`PulseCounter.PulseCounter`).
- An HLA cannot read raw channel samples. It only receives frames from a lower-level analyser. The edge source is Logic's built-in **Simple Parallel** analyser, which emits one frame per clock edge.
- `PulseCounter.decode()` is called once per input frame. It increments the total, and when a frame arrives at least `gate_ms` after the window start it returns one `count` frame spanning that window and prints the total to the Logic Terminal.
- Consequence: output only happens when a pulse arrives. With no pulses there are no bubbles and no prints, and the last partial window is reported on the next edge.
- Logic creates a fresh instance per capture (including every loop in looping trigger mode), so the total resets each capture.
- The Terminal print uses a leading `\r` with `end=''` so the total overwrites one line. Logic's Terminal honours `\r`.

## Setup facts learned on the bench
- Simple Parallel: set **Clock** (below D15) to the pulse channel with Clock State = Rising edge. **D0 must be a different, spare channel**. Using the clock channel for D0 gives "Invalid channel(s)".
- Untick Simple Parallel's **Stream to terminal**, otherwise its `\0` output floods the Terminal and breaks the single-line total.
- Double counting was traced to a ~25 ns bounce on the falling edge of the signal, which looks like an extra rising edge. Fix it with the Logic device **Glitch Filter** (100 ns on the channel), not in code.
- After editing `PulseCounter.py`, Logic does not reload a running analyser. Remove and re-add the Pulse Counter analyser, or restart Logic 2.
