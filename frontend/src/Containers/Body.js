import { useEffect, useState } from "react";
import Button from "@material-ui/core/Button";
import CircularProgress from "@mui/material/CircularProgress";

import styled from "styled-components";
import TextField from "@material-ui/core/TextField";

import { useStyles } from "../hooks";
import axios from "../api";

const Wrapper = styled.section`
  display: flex;
  flex-direction: column;
`;

const Row = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 1em;
`;

const Body = () => {
  const classes = useStyles();

  const [url, setUrl] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (func) => (event) => {
    func(event.target.value);
  };

  const handleSearch = async () => {
    setLoading(true);
    const {
      data: { transcribed },
    } = await axios.get("transcribe", { params: { url: url } });
    setContent(transcribed);
    setLoading(false);
  };

  const handleSummarize = async () => {
    setLoading(true);
    const {
      data: { summarized },
    } = await axios.get("summarize", { params: { content: content } });
    setContent(summarized);
    setLoading(false);
  };

  return (
    <Wrapper>
      <Row>
        <TextField
          style={{ width: "80%" }}
          className={classes.input}
          placeholder="Enter Google Podcast url..."
          value={url}
          onChange={handleChange(setUrl)}
        />
        {loading ? (
          <CircularProgress />
        ) : (
          <Button
            className={classes.button}
            variant="contained"
            color="primary"
            disabled={!url || loading}
            onClick={handleSearch}
          >
            轉錄
          </Button>
        )}
      </Row>

      <TextField
        id="standard-multiline-static"
        label="轉錄搞"
        multiline
        rows={20}
        defaultValue={content}
        variant="standard"
        onChange={handleChange(setContent)}
      />
      <Row justify="end">
        <Button
          disabled={loading}
          className={classes.button}
          variant="contained"
          color="primary"
          onClick={handleSummarize}
        >
          Summarize
        </Button>
      </Row>
    </Wrapper>
  );
};

export default Body;
