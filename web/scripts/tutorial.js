/* TUTORIAL FOR MEKUIDO by Leonardo Luarte */
// http://leonardo.luarte.net 

var Tutorial = new Class
				({
					askTutorial: function()
					{
						this.startTutorial();
						try
						{
							pageTracker._trackPageview('/tutorial/start');
						}catch(e){}
					},
					hideBubble: function()
					{
						var myFx = new Fx.Tween('bubble_container',{duration:'short',transition:'bounce:in',property:'opacity'});
						myFx.start(1,0);
					},
					showBubble:function()
					{
						var myFx = new Fx.Tween('bubble_container', {duration: 'long',transition: 'bounce:out',property: 'opacity'});
						myFx.start(0,1);
					},
					buildTwoWayMessage:function(text,text_for_option1,action_for_option1,text_for_option2,action_for_option2)
					{
						var m = {
							message: text,
							options:
							[
								{text:text_for_option1,action:Function.from(action_for_option1)},
								{text:text_for_option2,action:Function.from(action_for_option2)},
							]
						}
						return m;
					},
					
					showDialog:function(message)
					{
						if(message)
						{
							var bm = document.id('bubble_message');
							bm.empty();
							var p = new Element('p',{html:message.message, style:{'margin':'0px',}}).inject(bm);
							new Element('br').inject(p);
							for(var opt in message.options)
							{
								if(!message.options[opt] || message.options[opt].text == undefined) break;
								
								var option = message.options[opt]
								var linkAction = new Element('a',
									{
										href:'#'+option.text,
										events:
										{
											click: option.action.pass(1,this),
											
										},
										html: option.text,
										
									});
								var span = new Element('span');
								linkAction.inject(span);
								span.inject(p);
								
							}
							this.showBubble();
						}
					}
					,
					startTutorial:function()
					{
						var message = this.buildTwoWayMessage(	'Hola! Te daré un pequeño paseo por este menú para que conozcas el funcionamiento del sitio. ¿Empezamos?',
																'¡Empezar!',this.tutorialStep1,
																'Salir',this.hideBubble);
						this.showDialog(message);
					}
					,
					tutorialStep1:function()
					{
						var message = this.buildTwoWayMessage(	'Bien, primero en <strong>Que comí</strong> ingresas los alimentos consumidos el día anterior y calcular su aporte de calorías',
																'Seguir!',this.tutorialStep2,
																'Salir',this.hideBubble);
						this.showDialog(message);
					}
					,
					tutorialStep2:function()
					{
						var message = this.buildTwoWayMessage(	'La <strong>Trivia</strong> son preguntas para que revises tus conocimietos y prácticas relacionadas con alimentación y ejercicios.',
																'Seguir!',this.tutorialStep3,
																'Salir',this.hideBubble);
						this.showDialog(message);
					}
					,
					tutorialStep3:function()
					{
						var message = this.buildTwoWayMessage(	'Los  <strong>compromisos</strong> son un lugar para que anotes tus propios desafíos para mejorar tus prácticas',
																'Seguir!',this.tutorialStep4,
																'Salir',this.hideBubble);
						this.showDialog(message);
					}
					,
					tutorialStep4:function()
					{
						var message = this.buildTwoWayMessage(	'Finalmente, las <strong>Ayudas</strong> tienen material complementario que te ayudará a conocer más términos alimenticios, saber qué comidas son sanas y muchas cosas más.',
																'Ahora te invito a navegar por MeKuido!',this.hideBubble
																);
						this.showDialog(message);
					}
				});


function askTutorial()
{
	var t = new Tutorial();
	t.askTutorial();
}
