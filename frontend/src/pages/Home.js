import { Icon } from '@iconify/react';
import AudioReactRecorder, { RecordState } from 'audio-react-recorder';
// import axios from 'axios';
import React, { useState } from 'react';
import ReactAudio from 'react-audio-player';
import { Button, Spinner } from 'react-bootstrap';

const Home = () => {
  const [recordState, setRecordState] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState('አበበ በሶ በላ');

  const start = () => {
    setAudioBlob(null);
    setRecordState(RecordState.START);
  };

  const stop = () => {
    setRecordState(RecordState.STOP);
  };

  const onStop = (audioData) => {
    setAudioBlob(audioData);
  };

  const convertBase64 = (audioData) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(audioData);
      fileReader.onload = function () {
        resolve(fileReader.result);
        // console.log(e.target.result);
      };
      fileReader.onerror = function (e) {
        reject(e);
      };
    });
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const data = new FormData();
    console.log(audioBlob);
    data.append('file', audioBlob['url']);
    const blb = await convertBase64(audioBlob['blob']);
    // setMyad(blb);
    alert('Hi');
    console.log(blb);

    // Send the audio file to kafka as a json object
    // axios.post('http://localhost:8082/upload', data)
    fetch('http://localhost:8082/topics/kaf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/vnd.kafka.json.v2+json',
        // Accept: 'application/vnd.kafka.json.v2+json',
        // 'allow-origin': '*',
      },
      body: JSON.stringify({
        records: [{ value: { text, audio: blb } }],
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
    // let url = 'http://127.0.0.1:33507/predict';

    // axios.post(url, data).then((res) => {
    //   const { data } = res;
    //   console.log(data);
    //   // setTranscription(data.data);

    //   setLoading(false);
    // });
  };

  return (
    <div className="min-vh-100 d-flex flex-column justify-content-center align-items-center">
      <div className="text-center p-5">
        <h1 className="mb-4">Text from the corpus here...</h1>
        <div className="d-flex gap-3 justify-content-center">
          {recordState !== RecordState.START && (
            <Button
              onClick={start}
              variant="light"
              className="d-flex gap-2 align-items-center"
            >
              Record <Icon icon="el:record" />
            </Button>
          )}
          {recordState === RecordState.START && (
            <Button
              onClick={stop}
              variant="danger"
              className="d-flex gap-2 align-items-center"
            >
              Stop <Icon icon="carbon:stop-filled-alt" />
            </Button>
          )}
        </div>
        <div className="my-4">
          <AudioReactRecorder
            state={recordState}
            onStop={onStop}
            backgroundColor="white"
            foregroundColor="red"
            canvasWidth="500"
            canvasHeight="150"
          />
        </div>
        {!!audioBlob && (
          <div className="mb-4">
            <ReactAudio src={audioBlob['url']} controls />
          </div>
        )}
        {!!audioBlob && (
          <Button type="submit" variant="danger" onClick={(e) => submit(e)}>
            {loading ? (
              <Spinner animation="border" size="sm" />
            ) : (
              <span className="d-flex gap-2 align-items-center">
                Upload <Icon icon="akar-icons:cloud-upload" />
              </span>
            )}
          </Button>
        )}
      </div>
    </div>
  );
};
export default Home;
