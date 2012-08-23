function makeScrollbar(content,scrollbar,handle,horizontal,ignoreMouse){
	var steps = (horizontal?(content.getScrollSize().x - content.getSize().x):(content.getScrollSize().y - content.getSize().y))
	var slider = new Slider(scrollbar, handle, {	
		steps: steps,
		mode: (horizontal?'horizontal':'vertical'),
		onChange: function(step){
			// Scrolls the content element in x or y direction.
			var x = (horizontal?step:0);
			var y = (horizontal?0:step);
			content.scrollTo(x,y);
		}
	}).set(0);
	if( !(ignoreMouse) ){
		// Scroll the content element when the mousewheel is used within the 
		// content or the scrollbar element.
		$$(content, scrollbar).addEvent('mousewheel', function(e){	
			e = new Event(e).stop();
			var step = slider.step - e.wheel * 30;	
			slider.set(step);					
		});
	}
	// Stops the handle dragging process when the mouse leaves the document body.
	$(document.body).addEvent('mouseleave',function(){slider.drag.stop()});
}