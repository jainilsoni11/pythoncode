var imgArray = [],
curIndex=0;
imgDuration=1000;

function slideShow()
{
	document.getElementById('image1').src = imgArray[curIndex];
    curIndex++;
    if(curIndex == imgArray.length)
        {
            curIndex=0;
        }
    setTimeout("slideShow",imgDuration);
}
slideShow();