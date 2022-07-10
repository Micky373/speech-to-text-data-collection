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
  const [textLoading, setTextLoading] = useState(false);
  const [text, setText] = useState('');

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

  const getText = async () => {
    setTextLoading(true);

    let data = await fetch('http://localhost:8082/consumers/raw', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/vnd.kafka.v2+json',
      },
      body: JSON.stringify({
        name: 'my_consumer_instance',
        format: 'json',
        'auto.offset.reset': 'earliest',
      }),
    });
    data = await data.json();
    console.log('data1: ', data);
    data = await fetch(
      'http://localhost:8082/consumers/raw/instances/my_consumer_instance/subscription',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/vnd.kafka.v2+json',
        },
        body: JSON.stringify({ topics: ['raw'] }),
      }
    );
    // data = await data.json();
    console.log('data2: ', data.status);
    console.log('Data2222222222222222');
    data = await fetch(
      'http://localhost:8082/consumers/raw/instances/my_consumer_instance/records',
      {
        headers: {
          Accept: 'application/vnd.kafka.json.v2+json',
        },
      }
    );
    const json = await data.json();
    console.log(json);
    // check if there is data
    if (json.length > 0) {
      console.log(true);
      const text = json[0].value;
      console.log(text);
      setText(json[0].value.text);
    }
    await fetch(
      'http://localhost:8082/consumers/raw/instances/my_consumer_instance',
      {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/vnd.kafka.v2+json',
        },
      }
    );
    setTextLoading(false);
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const data = new FormData();
    console.log(audioBlob);
    data.append('file', audioBlob['url']);
    const blb = await convertBase64(audioBlob['blob']);
    // setMyad(blb);
    // alert('Hi');
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

    setLoading(false);
    // });
  };

  return (
    <div className="min-vh-100 d-flex flex-column justify-content-center align-items-center">
      <Button className="text-center p-2" onClick={getText}>
        {' '}
        {textLoading ? (
          <Spinner animation="border" size="sm" />
        ) : (
          <span className="d-flex gap-2 align-items-center">GET TEXT</span>
        )}
      </Button>
      <div className="text-center p-5">
        <h1 className="mb-4">{text}</h1>
        <div className="d-flex gap-3 justify-content-center">
          {recordState !== RecordState.START && (
            <Button
              onClick={start}
              variant="light"
              className="d-flex gap-2 align-items-center"
              // if there is text make it active otherwise make it disabled
              disabled={text === ''}
              // text !== '' ? disabled : active
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
