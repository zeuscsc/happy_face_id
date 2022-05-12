const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const lock = document.getElementsByClassName('lock')[0];
const canvasCtx = canvasElement.getContext('2d');
const classifier = knnClassifier.create();
const add_train_samples_buttons = document.getElementsByClassName('add_train_samples')
const MOVING_AVERAGE_LENGTH=10
let normalizedLandmarks=[];
let averageFacialExpression=5;
let initialized=false;
let hasLeftSmile=false;
let hasRightSmile=false;
let detecting=false;
(function trainingButtonEvents(){
  let id=0
  for(const button of add_train_samples_buttons){
    button.localStorageName=`class_${id}_training_samples`;
    button.addEventListener('click',(e)=>{
      const className=e.target.localStorageName;
      let samples=JSON.parse(localStorage.getItem(className));
      if (samples==null)
        samples=[];
      samples.push(normalizedLandmarks);
      localStorage.setItem(className,JSON.stringify(samples));
    })
    id++;
  }
})();
(function knnClassifierInit(){
  let id=0
  for(const button of add_train_samples_buttons){
    let samples=JSON.parse(localStorage.getItem(button.localStorageName));
    if(!samples)samples=training_samples[id];
    if(samples){
      for(const sample of samples){
        classifier.addExample(tf.tensor(sample), id);
      }
      initialized=true;
    }
    id++;
  }
})();
async function identityClassifier(image){
  detecting=true;
  let image_base64 = image.toDataURL('image/jpeg').replace(/^data:image\/jpeg;base64,/, "");
  let results=await fetch("http://127.0.0.1:8000/get-identity", {
    method: "POST",
    body: image_base64
  });
  let identity=await results.json();
  console.log(identity)
  detecting=false;
}
async function detectFacialExpression(image,normalizedLandmarks){
  if(initialized){
    const result=await classifier.predictClass(tf.tensor(normalizedLandmarks));
    averageFacialExpression -= averageFacialExpression / MOVING_AVERAGE_LENGTH;
    averageFacialExpression += result.label / MOVING_AVERAGE_LENGTH;
    const facialExpression=Math.round(averageFacialExpression)
    console.log(facialExpression);
    if(facialExpression==0)
      hasLeftSmile=true;
    if(facialExpression==1)
      hasRightSmile=true;
    if((facialExpression===4||facialExpression===0||facialExpression===1)&&hasLeftSmile&&hasRightSmile){
        lock.style.display="none";
        if(!detecting)
          identityClassifier(image)
        // const imageToBlob=new Promise((resolve, reject) =>{
        //   image.toBlob(async (blob)=>{
        //     resolve(blob);
        //   },'image/jpeg',1);
        // });
        // const blob=await imageToBlob;
        // const url = URL.createObjectURL(blob);
        // console.log(url);
        // let results=await fetch("http://127.0.0.1:8000/test", {
        //   method: "POST",
        //   body: url
        // });
    }
    if(facialExpression===5){
        lock.style.display="block";
        hasLeftSmile=false;
        hasRightSmile=false;
    }
  }
}

function onResults(results) {
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);
  if (results.multiFaceLandmarks) {
    for (const landmarks of results.multiFaceLandmarks) {
      const X=landmarks.filter(landmark =>landmark.x).reduce((total, next) => total + next.x, 0) / landmarks.length;
      const Y=landmarks.filter(landmark =>landmark.y).reduce((total, next) => total + next.y, 0) / landmarks.length;
      normalizedLandmarks=[];
      for(const landmark of landmarks) {
        normalizedLandmarks.push([landmark.x-X,landmark.y-Y]);
      }
      detectFacialExpression(results.image,normalizedLandmarks)
      
      // drawConnectors(canvasCtx, landmarks, FACEMESH_TESSELATION,
      //                {color: '#C0C0C070', lineWidth: 1});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_RIGHT_EYE, {color: '#FF3030'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_RIGHT_EYEBROW, {color: '#FF3030'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_RIGHT_IRIS, {color: '#FF3030'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_LEFT_EYE, {color: '#30FF30'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_LEFT_EYEBROW, {color: '#30FF30'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_LEFT_IRIS, {color: '#30FF30'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_FACE_OVAL, {color: '#E0E0E0'});
      // drawConnectors(canvasCtx, landmarks, FACEMESH_LIPS, {color: '#E0E0E0'});
    }
  }
  canvasCtx.restore();
}



const faceMesh = new FaceMesh({locateFile: (file) => {
  return `mediapipe/${file}`;
}});
faceMesh.setOptions({
  maxNumFaces: 1,
  refineLandmarks: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});
faceMesh.onResults(onResults);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await faceMesh.send({image: videoElement});
  },
  width: 1280,
  height: 720
});
camera.start();