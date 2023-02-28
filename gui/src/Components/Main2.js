import React, { useState } from "react";
import Tesseract from "tesseract.js";
import axios from "axios";

function Main() {
  const [summaryArticle, setSummaryArticle] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [extractedText, setExtractedText] = useState("");
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [summaryLines, setSummaryLines] = useState(0);

  const handleTextArea = (value) => {
    setExtractedText(value);
  };
  // handle image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImageFile(file);
    setImagePreviewUrl(URL.createObjectURL(file));
  };

  // handle image extraction
  const handleImageExtraction = () => {
    Tesseract.recognize(imageFile, "eng").then(({ data: { text } }) => {
      setExtractedText(text);
      //setExtractedTextTextArea(text)
    });
  };

  const handleSummaryTextArea = (value) => {
    setSummaryArticle(value);
  };
  const handleLinesChange = (value) => {
    setSummaryLines(value);
  };

  const sendExtractedText = () => {
    const endpoint = "http://localhost:8000/api/";
    console.log("Sending data");
    const json_data = {
      title: "",
      article: extractedText,
      lines: summaryLines,
    };
    console.log(json_data);
    axios
      .post(endpoint, json_data)
      .then((res) => {
        console.log("data fetched: ");
        console.log(res);
        setSummaryArticle(res.data.summary);
      })
      .catch((err) => {
        console.log("Error occured");
        console.log(err);
      });
  };

  return (
    <div className="container">
      <div className="hero-section">
        <h2 className="heading">
          Transform Images into Clear and Concise Summaries with Our Image-Text
          Summarization Tool
        </h2>

        <div>
          <input
            className="input-section"
            type="file"
            // accept=".pdf .png .jpeg .jpg .tiff"
            onChange={handleImageUpload}
          />
        </div>
        {imagePreviewUrl && (
          <div>
            <img src={imagePreviewUrl} style={{ maxWidth: "20%" }} />
          </div>
        )}

        <div>
          <button className="convert" onClick={handleImageExtraction}>
            Convert
          </button>

          <div className="group-one">
          <p className="btn-heading">Enter the number of lines of summary yuo want</p>
            <input
              className="input-lines"
              type="number"
              placeholder="Number of lines of summary"
              value={summaryLines}
              onChange={(e) => handleLinesChange(e.target.value)}
            />

            <button
              className="submit-button"
              type="submit"
              onClick={() => sendExtractedText()}
            >
              Summarize
            </button>
          </div>

          {/* <div>
            <div className="lds-ring">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
            <p className="loading">Loading...</p>
          </div> */}
        </div>

        <div className="output-box">
          <div>
            <div className="output-one">
              <textarea
                placeholder=" Text Extracted or Paste any Article, Paragraph directly"
                value={extractedText}
                onChange={(e) => handleTextArea(e.target.value)}
              ></textarea>
            </div>
          </div>
          {/* <label for="quantity">Quantity (between 1 and 5):</label> */}

          <div className="output-two">
            <textarea
              placeholder="  Genrated Summary"
              value={summaryArticle}
              onChange={(e) => handleSummaryTextArea(e.target.value)}
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Main;
