
var myFx = new Fx.Tween('bubble_container', {
duration: 'long',
transition: 'bounce:out',
property: 'opacity'}
);
var closeBubble = $('closeBubble');
closeBubble.addEvent('click',function(){
	myFx.start(1,0);
});
