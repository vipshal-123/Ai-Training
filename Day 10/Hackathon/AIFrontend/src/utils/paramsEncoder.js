export default function paramsEncoder(object) {
  return new URLSearchParams(object).toString();
}