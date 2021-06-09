import { Component, OnInit } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {


  jsonFormObject: any;

  constructor(
    private http: HttpClient
  ) { }

  ngOnInit(): void {
    const schemaURL = `assets/schemas/user.json`;
    this.http
      .get(schemaURL, { responseType: 'text' })
      .subscribe(schema => {
        this.jsonFormObject = JSON.parse(schema);
      });

  }

 submitForm(data: any) {
    	let headers_object = new HttpHeaders({});
    	headers_object = headers_object.append('Content-Type', 'application/json');
	headers_object = headers_object.append('Authorization', 'Basic ' + btoa('admin:secret'));
	const httpOptions = {
	      headers: headers_object
	    };
	this.http
	      .post('http://127.0.0.1:8080/collection', data, httpOptions).subscribe();
  }

}
