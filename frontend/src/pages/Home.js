import { Icon } from "@iconify/react";
import AudioReactRecorder, { RecordState } from "audio-react-recorder";
// import axios from "axios";
import React, { useState } from "react";
import ReactAudio from "react-audio-player";
import { Button, Spinner } from "react-bootstrap";

const Home = () => {
    const [recordState, setRecordState] = useState(null);
    const [audioBlob, setAudioBlob] = useState(null);
    const [loading, setLoading] = useState(false);

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

    const submit = () => {
        setLoading(true);
        const data = new FormData();
        data.append("file", audioBlob["blob"]);
        // let url = "http://localhost:5000/predict";

        // axios.post(url, data).then((res) => {
        //     const { data } = res;

        //     setTranscription(data.data);

        //     setLoading(false);
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
                        <ReactAudio src={audioBlob["url"]} controls />
                    </div>
                )}
                {!!audioBlob && (
                    <Button
                        type="submit"
                        variant="danger"
                        onClick={() => submit()}
                    >
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
