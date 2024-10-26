function base64ToBytes(base64) {
    const binString = atob(base64);
    return Uint8Array.from(binString, (m) => m.codePointAt(0));
}
  
function bytesToBase64(bytes) {
    const binString = Array.from(bytes, (byte) =>
      String.fromCodePoint(byte),
    ).join("");
    return btoa(binString);
}

export function strToBase64(str) { return bytesToBase64(new TextEncoder().encode(str)); }
export function base64ToStr(base64) { return new TextDecoder().decode(base64ToBytes(base64)); }