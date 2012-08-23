//Implode and Explode
dojo.require("dojo.fx");
function closeNamedElement(name)
{
	var animation = dojo.animateProperty(
	    {
	      node: name,duration: 200,
	      properties: {
		height: {end: 1}

	      }
	    });
	animation.play();
}
function closeAllElements()
{
	closeNamedElement('puestosDescription');
	closeNamedElement('donacionesDescription');
	closeNamedElement('amigosDescription');
	closeNamedElement('profesionalesDescription');
}
function toggleExplodiableElement(nodeName,partner,otherElement,thisElement,size)
{
	closeAllElements();
	var e = document.getElementById(nodeName);
	var _otherElement = document.getElementById(otherElement);
	var _thisElement = document.getElementById(thisElement);
	var _height= size;
	console.log(document.getElementById(partner).style.height);
	//if(document.getElementById(partner).style.height != "1px")
	//	toggleExplodiableElement(partner,nodeName,otherElement,thisElement,size);
	console.log("Applying...");
	console.log(e.style.height);
	if( parseInt(e.style.height) != 1)
	{
		_height = 1;
		console.log("must minimize and invert elements");
		var temp = otherElement;
	}
	
	
	
	var animation = dojo.animateProperty(
	    {
	      node: nodeName,duration: 1000,delay:150,
	      properties: {
		height: {end: _height}
	      }
	    });
	var unfocusElement = dojo.animateProperty({
		node: otherElement, duration: 500,
		properties: {
			width: {end: 150}
		}
	});
	var focusElement = dojo.animateProperty({
		node: thisElement, duration: 500,
		properties: {
			width: {end: 350}
		}
	});
	unfocusElement.play();
	focusElement.play();
	animation.play();
	var action = null;
	
	
	
	
}