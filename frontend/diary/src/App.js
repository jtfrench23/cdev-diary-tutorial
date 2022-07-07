import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from "react";

function App() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [entrys, setEntries] = useState([]);
  const endpoint = "https://980e0oj2pl.execute-api.us-east-1.amazonaws.com/live"
  useEffect(() => {
    const getEntries = async() => {
        const entry_Data = await fetch(
            "https://980e0oj2pl.execute-api.us-east-1.amazonaws.com/live/entry/get",
            {
            headers: {
                "Content-Type": "application/json"
                },
            }
        );
        const entryData = await entry_Data.json();
        console.log(entryData, "this one")
        setEntries(entryData)
        console.log(entrys)
    }
    getEntries();
}, []);

const handleSubmit = (e) => {
  e.preventDefault();
  console.log("function running")
  const createEntry = async () => {
      try {
      const entryData = await fetch(
          "https://980e0oj2pl.execute-api.us-east-1.amazonaws.com/live/entry/create",
          {
          method: "POST",
          headers: {
              'Content-Type': 'application/json',
          },
          body:JSON.stringify({
              "title":title,
              "content":content
          })
          }
      );
      const entry_info = await entryData.json();
      console.log(entry_info);
      } catch (e) {
      console.log(e.message);
      }
      window.location.reload(true);
  };
  createEntry();
}
  return (
    <div className="App">
      <form  onSubmit={handleSubmit}>
        <h2>Create New Entry</h2>
          <div className="form-group col">
            <input
                className="form-control org-input px-1 pr-1"
                type="text"
                htmlFor="title"
                aria-label="Title"
                name="title"
                placeholder="Title"
                // following two lines update the state with the inputs from the user
                value={title}
                onChange={event => setTitle(event.target.value)}
            />
          </div>
          <div className="form-group col">
            <input
                className="form-control org-input px-1 pr-1"
                type="text"
                htmlFor="content"
                aria-label="Content"
                name="content"
                placeholder="Content"
                // following two lines update the state with the inputs from the user
                value={content}
                onChange={event => setContent(event.target.value)}
            />
          </div>
          <button
          className="btn btn-success org-input px-1 pr-1 mr-2"
          type="submit"
          >
              SUBMIT
          </button>
      </form>
      <div>
        <h2>Entries</h2>
        {posts.length>0 &&
          posts.map((item, i) =>
          <div key={i}>
            <h3>{item.title}</h3>
            <p>{item.content}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
