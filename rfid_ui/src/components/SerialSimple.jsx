// SerialSimple.js
// Minimal helper for the Web Serial API — no UI, just a simple function.
// - Usage must be triggered by a user gesture (browser requires requestPort() inside a click).
// - Works in Chromium-based browsers on HTTPS or localhost.

export async function openSerialSimple(baudRate = 9600, onData) {
  if (!('serial' in navigator)) throw new Error('Web Serial API not supported in this browser');

  // Ask user to pick the port
  const port = await navigator.serial.requestPort();

  // Open with the selected baud rate (browsers may only honor baudRate)
  await port.open({ baudRate: Number(baudRate) });

  const decoder = new TextDecoderStream();
  const readableClosed = port.readable.pipeTo(decoder.writable);
  const reader = decoder.readable.getReader();

  let stopped = false;

  // Start background read loop
  (async () => {
    try {
      while (!stopped) {
        const { value, done } = await reader.read();
        if (done) break;
        if (value !== undefined) {
          try {
            if (typeof onData === 'function') onData(value);
          } catch (e) {
            console.error('onData callback error', e);
          }
        }
      }
    } catch (err) {
      console.error('Read loop error:', err);
      if (typeof onData === 'function') onData(null, err);
    }
  })();

  // Provide disconnect helper
  const disconnect = async () => {
    stopped = true;
    try { await reader.cancel(); } catch (e) {}
    try { await readableClosed; } catch (e) {}
    try { await port.close(); } catch (e) {}
  };

  return { disconnect };
}
