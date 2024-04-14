import React , {useRef, useState} from 'react';
import { Robot, Robot2, arrowDown, file } from '../assets';
import styles from '../style';
import GetStarted from './GetStarted';
import axios from "axios";

function Hero(){

  const ref1 = useRef(null);
  const ref2 = useRef(null);
  const ref3 = useRef(null);
  const ref4 = useRef(null);

  function startedClick(){
    ref1.current.focus();
    ref1.current.style.visibility = "visible";
    ref2.current.style.visibility = "visible";
    ref3.current.style.display = "block";
    ref4.current.style.display = "block";
  }

  //const payload = {message: null};
  const [x, setx] = useState(0);

  const [markdownContent, setMarkdown] = useState(null);
  const [payload, setPayload] = useState(null);

  const headers = {
    'Openai-key': '##################################'
  };

  const downloadMarkdown = () => {
    const element = document.createElement('a');
    const file = new Blob([markdownContent], {type: 'text/markdown'});
    element.href = URL.createObjectURL(file);
    element.download = 'document.md';
    document.body.appendChild(element);
    element.click();
  };

  async function postDoc(){
    const response = await axios.post("https://documentationgenerator.applikuapp.com/askdoc", payload, { headers });
    console.log(response.data.response);
    setMarkdown(response.data.response);
    setx(1);
  }

  async function postUpdate(){
    const response = await axios.post("https://documentationgenerator.applikuapp.com/askupdate", payload, { headers });
    console.log(response.data.response);
    setMarkdown(response.data.response);
    setx(2);
  }

  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      // Check if the file type is text/plain (i.e., a text file)
      // if (file.type === 'text/plain') {
      if (1==1) {  
        const reader = new FileReader();
        reader.onload = (e) => {
          // Display the content of the text file
          
          setPayload({message: e.target.result});
          console.log('File Content:', payload);
        };
        reader.readAsText(file);
      } else {
        console.log('Unsupported file type. Please upload a text file.');
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <section id='home' className={`flex md:flex-row flex-col ${styles.paddingY}`}>

        <div className={`flex-1 ${styles.flexStart} flex-col xl:px-0 sm:px-16 px6`}>

            <div className='flex flex-row justify-between items-center w-full'>
                <h1 className='flex-1 font-poppins font-semibold ss:text-[72px] text-[52px] text-white ss:leading-[100px] leading-[75px]'>The Next <br className='sm:block hidden'/> {" "}
                    <span className='text-gradient'>Generation</span> {" "}
                </h1>
                <div className='ss:flex hidden md:mr-4 mr-0' onClick={startedClick}>
                    <GetStarted ></GetStarted>
                </div>
        </div>

        <h1 className='flex-1 font-poppins font-semibold ss:text-[72px] text-[52px] text-white ss:leading-[100px] leading-[75px] w-full'>Documentation Generator</h1>

        <p className={`${styles.paragraph} max-w-[640px]`}>Our dedicated team of software engineers recognises the precious time of developers and so we give you this tool for automatically generating your documentation.</p>
        <div className='mt-[10px]'>
          <div className='w-[300px] h-[50px] mt-[10px] text-gradient text-[30px] cursor-pointer' onClick={postUpdate}>Code Improvements</div>
          {x==2 && (
            <button className='absolute w-[80px] h-[80px] mt-[3%] ml-[24%] z-[8]' onClick={() => downloadMarkdown()}><img src={file} alt="file" className='w-[80px] h-[80px]' /></button>
          )}
          <img src={Robot2} alt="Robot2" />
        </div>

      </div>

      <div className={`flex-1 flex ${styles.flexCenter} md:my-0 my-10 relative`}>
        
        <div className='flex flex-col items-center'>
          {x==1 && (
            <button className='absolute w-[80px] h-[80px] mt-[45%] mr-[70%] z-[8]' onClick={() => downloadMarkdown()}><img src={file} alt="file" className='w-[80px] h-[80px]' /></button>
          )}
          <div className='absolute w-[200px] h-[50px] mt-[75%] mr-[50%] z-[8] text-gradient text-[30px] cursor-pointer' onClick={postDoc}>Documentation</div>
          <div className='z-[2] mb-[5px] ml-[30%] text-gradient text-[30px] invisible' ref={ref1}>Upload File</div>
          <img src={arrowDown} alt="arrow down" className='w-[44px] h-[44px] ml-[30%] invisible z-[7]' ref={ref2} />
          <form className='w-[190px] h-[190px] rounded-full border-dashed z-[8] border-4 absolute mt-[17%] ml-[30%] hidden cursor-pointer' action="" onClick={handleButtonClick} ref={ref3}>
            <input type="file" className='input-field hidden' ref={fileInputRef} onChange={handleFileChange} />
          </form>
          <img src={Robot} alt="robot" className='w-[90%] h-[90%] mt-[5px] relative z-[7]' />

        </div>

        <div className='absolute z-[0] w-[40%] h-[35%] top-0 pink__gradient' />
        <div className='absolute z-[1] w-[80%] h-[80%] rounded-full bottom-40 white__gradient' />
        <div className='absolute z-[0] w-[50%] h-[50%] right-20 bottom-20 blue__gradient' />
      </div>



    </section>
  )
}

export default Hero