import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'my-app';

 submitForm(data: any) {
    /**
	let headers_object = new HttpHeaders({});
    	headers_object = headers_object.append('Content-Type', 'application/json');
	headers_object = headers_object.append('Authorization', 'Basic ' + btoa('admin:changeit'));
	const httpOptions = {
	      headers: headers_object
	    };
	    this.http
	      .post('http://127.0.0.1:8080/db/users', data, httpOptions);
	**/
  }

exampleJsonObject = {
  "first_name": "Jane", "last_name": "Doe", "age": 25, "is_company": false,
  "address": {
    "street_1": "123 Main St.", "street_2": null,
    "city": "Las Vegas", "state": "NV", "zip_code": "89123"
  },
  "phone_numbers": [
    { "number": "702-123-4567", "type": "cell" },
    { "number": "702-987-6543", "type": "work" }
  ], "notes": ""
};

}


