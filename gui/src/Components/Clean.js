import React from "react";

function Clean({ extractedText }) {
  const cleanedText = extractedText
    // remove non-printable characters
    .replace(/[^\x20-\x7E]/g, "")
    // remove hyphens and join split words
    .replace(/(-|\n)[\s]*/g, "")
    // remove extra spaces
    .replace(/\s+/g, " ")
    // add spaces around punctuation
    .replace(/([,.?!:;])/g, " $1")
    // remove leading and trailing spaces
    .trim();

  return (
    <div>
      <textarea className="output-2" value={cleanedText} readOnly></textarea>
    </div>
  );
}

export default Clean;
