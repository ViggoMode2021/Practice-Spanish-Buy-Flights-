//Check the inputs to see if we should keep the label floating or not
const inputs = document.forms['date-input-form'].elements;

for (let i = 0; i < inputs.length; i++) {
	
	inputs[i].addEventListener('blur', function() {
		
		//Different validation for different inputs
		switch(this.tagName) {
			case 'SELECT': 
				if (this.value > 0) {
					this.className = 'hasInput';
				} else {
					this.className = '';
				}
				break;
				
			case 'INPUT':
				if (this.value !== '') {
					this.className = 'hasInput';
				} else {
					this.className = '';
				}
				break;
				
			default: 
				break;
		}
	});		
}


//Reset button
const reset = document.getElementById('reset');

reset.addEventListener('click', event => {
	
	event.preventDefault();
	
	for (let i = 0; i < inputs.length; i++) {
		inputs[i].className = '';
		inputs[i].value = '';
	}
	
	console.log('Forms reset.');
	return false;
});
