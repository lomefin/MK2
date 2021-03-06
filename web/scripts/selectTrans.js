var selectTrans = new Class({
	
	Implements: [Options],
	
	options: {
		transition: [
			'select',
			'linear',
			'quad:in', 'quad:out', 'quad:in:out',
			'cubic:in', 'cubic:out', 'cubic:in:out',
			'quart:in', 'quart:out', 'quart:in:out',
			'quint:in', 'quint:out', 'quint:in:out',
			'expo:in', 'expo:out', 'expo:in:out',
			'circ:in', 'circ:out', 'circ:in:out',
			'sine:in', 'sine:out', 'sine:in:out',
			'back:in', 'back:out', 'back:in:out',
			'bounce:in', 'bounce:out', 'bounce:in:out',
			'elastic:in', 'elastic:out', 'elastic:in:out'
		 ],
		 duration: [
			'select',
			'short', 'normal', 'long'
		],
		commonFx: [
			'select',
			'blind:up', 'blind:down', 'blind:left', 'blind:right',
			'slide:up', 'slide:down', 'slide:left', 'slide:right'
		],
		panelStartFx: ['fade'],
		panelEndFx: ['fade']
	},
 
	initialize: function(element,fx) {
		
		var divs = $$('#' + element + ' div');
		
		divs.each(function(element) {
			
			var selectOptions = null;
			
			var selectBox = new Element('select').inject(element);
			
			var opt = element.id.split("_");
			
			if (opt[0].contains('Fx')) {
				this.fx = [];
				
				this.fx = this.options.commonFx;
				if (opt[0].contains('Start')) {
					selectOptions = this.fx.include(this.options.startFx);
				} else {
					selectOptions = this.fx.include(this.options.endFx).erase(this.options.startFx);
				}
			} else {
				selectOptions = this.options[opt[opt.length - 1]];
			}
			
			selectOptions.each(function(selectValue) {
				new Element('option', {
					'value': selectValue,
					'text': selectValue
				}).inject(selectBox);
			});
			
			var selectChange = selectBox.retrieve('selectBox:change', this.elementChange.bindWithEvent(this, fx));
			
			selectBox.addEvents({
				change: selectChange
			});
		},this);
	},
 
	elementChange: function(event, fx) {
		var event = new Event(event).stop();
		var changeValue = event.target.get('value');
		var opt = event.target.getParent().id.split("_");
		if (opt.length == 1) {
			fx.elSwap.options[opt[0]] = changeValue;
		} else {
			options = {};
			options[opt[1]] = changeValue
			fx.elSwap.changeFx('all', options);
		}
	}
});