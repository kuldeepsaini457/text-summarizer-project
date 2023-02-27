// import React, { useState } from "react";
// import LanguageTool from "languagetool";
// import { Button, Input, Row, Col, Typography } from "antd";

// const { TextArea } = Input;
// const { Title } = Typography;

// const Main = () => {
//   const [inputText, setInputText] = useState("");
//   const [processedText, setProcessedText] = useState("");

//   const handleFileUpload = (event) => {
//     const file = event.target.files[0];
//     const reader = new FileReader();

//     reader.readAsText(file);

//     reader.onload = (event) => {
//       setInputText(event.target.result);
//     };
//   };

//   const handleTextChange = (event) => {
//     setInputText(event.target.value);
//   };

//   const handleConvertClick = async () => {
//     const languageTool = new LanguageTool({ language: "en-US" });
//     const { matches } = await languageTool.check(inputText);

//     let newProcessedText = inputText;

//     matches.forEach((match) => {
//       const { offset, length, message } = match;

//       newProcessedText = [
//         newProcessedText.slice(0, offset),
//         message,
//         newProcessedText.slice(offset + length),
//       ].join("");
//     });

//     setProcessedText(newProcessedText);
//   };

//   return (
//     <>
//       <Row justify="center" align="middle" style={{ marginTop: "20px" }}>
//         <Col span={24} md={12}>
//           <Title level={2}>Text Processing and Grammar Checking</Title>
//           <Input type="file" onChange={handleFileUpload} />
//           <TextArea rows={10} value={inputText} onChange={handleTextChange} />
//           <Button type="primary" onClick={handleConvertClick}>
//             Convert
//           </Button>
//         </Col>
//         <Col span={24} md={12}>
//           <Title level={2}>Processed Text</Title>
//           <TextArea rows={10} value={processedText} />
//         </Col>
//       </Row>
//     </>
//   );
// };

// export default Main;
