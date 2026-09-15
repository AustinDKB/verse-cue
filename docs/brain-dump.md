Pro Presenter Auto Advance System.

Pro pResenter api: https://openapi.propresenter.com
Should be atleast 2 methods that are useful for this: Read Current SLide, and Advance ot next slide:

Also we should use WhisperX for Word LEvel Timestamps.
WHats the msot accurate we can acivehve but still be atleast 4x real time speed?
Me when I do the slide changes personally I wait for the person to have started the last sylabol on the last word of the slide. Or the last word if its a single sylsabol. 
Then we switch teh slide. Also we need to be careful as osme slides have repeated words many time or repeated sentences as well 

We should make sure that we have a list of aliases as these models werent meant for singing transcription for more accurate desciriptions.

We could have multiple transcriptions streams per loaded model to pin point when to advance the slide.
Advancing early is always prefered to advancing late!

So Since I advance on the last slyabol we should maybe since there will be latency, we should when detecting the 3rd or 4th last word add x amount of time then advance the slide to take into account the latency.

We can figure out a good number of aliases by using the tiny model and using the shittiest settings to get any halluncations from songs, if that makes sense? Make tiny model intentionally halucinate. THen Have each real word have a dictionary of sorts that contains 10 to 20 hallucination options for the most commoon error prone words. 

We should be able to use YT music from my phone as an audio device and an subagent can work on that or something. For the intentional halluncaiton we should use the same sized chunks we will be feeding the main transcription model. Each slide takes approx 12 to 20 seconds. So chunks should be 3s I think? Challenge this assumption. Also for example first chunk will transcribe 0 to 3, Next 1.5s to 4.5s, then next 3.5s to 7s. All running at once. Once a slide it actually changed, make sure to scrap any thing that is being transcribed from the previous slide.

Also we will not have to store any song data since we can get the current slide data and then, use that as teh words. We will need to detect voice activity to be able to transition form blank slides which are used for the intrumnentaiton poritons of the song.

We will only have one single input for audio, Voice.

Ideal Constraints for the Python Logic:
Less than 500 SLOC, LESS IS MORE, DO WE ACTUALLY NEED THIS? THIS CODE
Must be readible by a human
Meets all Anti Slop Metrics
Uses MInimal External Libraries.
USE A TOML Config FIle. FOr all Configuation things, such as params for the Transcription MOdel
OTHER CONSTRAINTS:
Full Beautiful Read Me on Github
Using Rendered Graphs.
Published Public with a great name.
Along with a list of Metrics we will be recording and will publish after miltple runs being done. 
Create a MAX 180 second beautiful explainer video using Hyper Frames and a local voice model.
Do not attribute the AI Model
Prepare a few short Posts to schedule and share on the ProPresenter Facebook Page
make sure it can be installed in 5 steps or less for any one on Mac or Windows PC.
Ask for Input and other ideas from people. We should spec it so almost any hardware can work very well.
We should also publsih this original scrappy plan just more polished then the final plan after using super powers with Fable, then use DeepSeek V4.1 Flash to implment Fable5.1s plan. Publish costs to build.
ALso regarding Using mutlitple streams. if we record 3 s at a time one stream can be offset by 1.5s, and another offset by 3.5s? each 3second long to ensure we are catching the key words we will start timing the slide change to. We should also have multiple words we can start a timer off. Obviosiously preferring the word closest to the end of the slide. SO timer cna be over written by a later key words timer if that word is detected. Each slide change resets all timers and stored data about that slide. 

Also one more thing: reltated to creating halluncatiuon alias dictionary, we need to make sure it has little to no time to look up. Also I mentioned feeding YT Music into my PC as an audio source and you find the lyrics and create it. How many songs do U thin would need to play through to create enough Samples? it could run overnight if the system is reliable enough and deterministic enough with good tests. Soa  Mini Pipleine. This hsould get done tonight.


Yo this is all in addition to the Word doc that I typed about the ProPresenter auto advanced, just some ideas:
• Choose the model that is going to perform the best for the system. That is built to be automatically chosen and downloaded based on automatic testing and, before automatic testing, estimated based on the GPU or the CPU that is installed on the system.
• Minimising the logic lines of code. I would count what we just spoke about: the automatic deterministic decision for which Wispr model to use for testing.
• Compile or not compile, and include audio files for testing to determine the accuracy and speed of each model and determine which one to use based on minimum requirements to get the performance that you would want if you were using this.


To go along with that I'm not sure if those count as tests or if they count as production code but ideally I think we could potentially constrain the production code to 500 lines. Tests obviously can be more than that.

Really this is just one big loop with a configuration file for the model parameters, most of which will be systematically chosen, so someone should just be able to start the file. It'll look at your CPU and your GPU, determine the model size that it should use, the batch size, and things such as audio segments that it transcribes will be different lengths or be predetermined based on what I decide, what we find is best from research.

The 400-line code limit will not include aliases from generated hallucinations as well. That will be in some JSON file or something like that as storage for testing to make sure accuracy is good and speed is good.

We should use a variety of different song types and tempos, and ones with easier words and more difficult words, such as "Hallelujah." It's just a few of my thoughts to add to that other document for planning. I think this should be a pretty small project. It's a loop that reads and finds a couple of words that work well to match with. Based on those words when they're detected, we add a timer that will do the next slide, clear all previous transcriptions, and start over again. If, let's say, the third word is found, it starts a timer and then we find another word that works really well that's closer to the end of the slide, we would use that one instead. Of course on slide switch anything that was transcribing before for the previous slide we can discard and then we can restart a new batch of transcriptions. Also with blank audio we need to use voice activity detection to determine when wewhen we're on an instrumental slide, this should be one loop and a couple of requests. The only thing that the user should have to do is detect that or maybe change the port number in ProPresenter and that's it for them.

For the Wispr model choosing we can have all the models available as well as a couple of parameters that will automatically get chosen for more granularity. This should be a pretty basic script. It should be easy to understand and it shouldn't matter who's singing. It shouldn't matter what the song is.

IN ADDITION
MAYBE LIMIT TO 2 DELTA SCRIPTS
ADD THE OLD FOLDER AS REFENCE BUT THIS NEW FOLDER AND THIS FILE AS CANON.

WW CAN USE OLD FOLDER FOR WHAT WE WERW TRYING TO DO VS WHERE IT WNDED UP FOR THE PPRFOLIO REPORT AND READ ME

ADD ANTI SLOP MWNTRICS AND SUPER POWERS BEFOEE BUILDING
USE FABLE TO PLAN THEN AUTO TO BUILD

REFERENCE FOR OLD SHIT: /home/austin/Desktop/PP AutoV2
REPO FOR SPECS: https://github.com/AustinDKB/anti-slop-toolkit