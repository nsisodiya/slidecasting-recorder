#!/bin/bash

echo "####   Generating SlideCasting"
rm -rf ./output
unzip output.zip
mv ./SpeakerAudio.ogg ./output/files/
mv ./time.xml ./output/files/
convert ./slides.pdf ./output/files/img.png
#rm ./slides.pdf

echo "<!DOCTYPE html>
<html>
<head>
  <title>Eduvid Slidecasting</title>

  <link href=\"files/slide.css\" media=\"screen\" rel=\"stylesheet\" type=\"text/css\" />
  <script type=\"text/javascript\" src=\"files/jquery-1.6.min.js\"></script>  
  <script type=\"text/javascript\" src=\"files/popcorn.js\"></script>
  <script type=\"text/javascript\" src=\"files/popcorn.slide.js\"></script>
  <script type=\"text/javascript\" src=\"files/slidecasting.js\"></script>
</head>
<body>

  <div id=\"slidecasting\">
		  <div class=\"presentation\">" > ./output/demo.html


TotalSlides=`ls output/files/*.png | sort -n | cut -d"-" -f2 | cut -d"." -f1 | sort -nr | head -n 1`

for i in `seq 0 1 $TotalSlides`; do echo "			<div class=\"slide\"><img src=\"files/img-$i.png\"></img></div>" ; done >> ./output/demo.html


echo "		  </div>


		  <div class=\"video\">
		    <audio id='myaudio' 
		      controls preload='none'> 

		      <source id='ogg' src=\"files/SpeakerAudio.ogg\" type=\"audio/ogg\">

		      <p>Your user agent does not support the HTML5 Video element.</p> 

		    </audio> 
		  </div>

  </div>
<p>Generated from Eduvid Slidecasting Recorder - visit </p>
</body>
</html>" >> ./output/demo.html

echo "Successfully Done. Please open ./output/demo.html in Firefox "

exit 0
