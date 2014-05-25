slidecasting-recorder
=====================

WxPython based Slidecasting Recorder

= About =

WxPython based Slidecasting Recorder - A Product of ELPA Technologies


It is a presentation application. You can use ODP (Libreoffice) and PDF files. When you start recording a presetation. It will mix your Audio and Slide into HTML format. Please note that it will not generate video.
=Tutorial=
<wiki:video url="https://www.youtube.com/watch?v=vDM7QBGl6-4"/>
= Development =
How to use it (For Ubuntu 11.04) 


First install dependency list

    sudo apt-get install python-poppler python-wxgtk2.8 unoconv

Now download source code


    svn checkout http://slidecasting-recorder.googlecode.com/svn/trunk/ slidecasting-recorder
    cd slidecasting-recorder
    ./SlideCasting.py


This will open a GUI where you can open any ODP or PDF file and run start presentation.
It will generate Time.xml and Audio file.

= Demo =

* http://code.narendrasisodiya.com/video-slidecast/demo.html
