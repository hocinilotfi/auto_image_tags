
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './App.css';


import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState();
  const [image, setImage] = useState();
  const [result, setResult] = useState();
  const [error, setError] = useState();
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    if (!e.target.files[0]) return;
    setFile(e.target.files[0]);

    const img = URL.createObjectURL(e.target.files[0]);
    setImage(img);
    setResult(null);
    //handleSubmit();
  };

  const handleSubmit = async (event) => {
    setLoading(true);
    event.preventDefault();

    const formData = new FormData();
    formData.append("image", file);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post("http://localhost:8000/process_image/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log(response.data);
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setError(error);
      setLoading(false);
    }
  };
  return (
    <div className="App">
      <div className="container">
        <h2>Upload an image file</h2>
        <form onSubmit={handleSubmit}>

          <input
            type="file"
            id="file"
            name="file"
            onChange={handleChange}
            accept="image/jpeg, image/png"
          />
          <button type="submit" disabled={loading}>
            Guess Content
          </button>
        </form>
        {image && (
          <div className="image-container">
            <img src={image} alt="previz" />
          </div>
        )}
        {result && (
          <div className="result-container">
            This image may contain: <br />
            {result && result.data.map((item, index) => <p key={index}>{item}</p>)}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
