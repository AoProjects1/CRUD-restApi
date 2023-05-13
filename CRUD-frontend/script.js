let tbody = document.querySelector('tbody');
let addBtn = document.querySelector('.add');
let form = document.querySelector('.form-wrapper');
let saveBtn = document.querySelector('.save');
let cancelBtn =  document.querySelector('.cancel');
let personEmail =  document.querySelector('#per_email');
let personName =  document.querySelector('#per_name');
let personAge =  document.querySelector('#per_age');
let personGender =  document.querySelector('#per_gender');

let httpm =null;

let url ='http://localhost:5000/persons';

let persons =[];

let id=null;

let data ={};

addBtn.onclick = function(){
    httpm="POST";
    clearForm();
    form.classList.add('active')
}


cancelBtn.onclick = function(){
    form.classList.remove('active')
}

saveBtn.onclick= function(){

    data.email= personEmail.value;
    data.name= personName.value;
    data.age = personAge.value;
    data.gender = personGender.value;
    if(httpm=="PUT"){
        data.id= id
        url+=`/${id}`;
    }


    
    fetch(url,
        { 
            method: httpm, body: JSON.stringify(data), 
            headers: { "Content-type": "application/json" } 
        })
    .then(()=>{
        clearForm();
        form.classList.remove('active');
        url ='http://localhost:5000/persons';
        getPersons()
    })


}

function clearForm(){
    personEmail.value =null;
    personName.value =null;
    personAge.value= null;
    personGender.value =null;
}



function getPersons(){
    fetch(url)
    .then(response=>response.json())
    .then(data=>{
        persons = data;
        updateTable();

    })

    
}

getPersons();

function updateTable(){
    let data="";

    if(persons.length>=0){
        for(i= 0;i<persons.length;i++){

            data+=  `<tr id="${persons[i]['id']}">
                        <td>${persons[i]['id']}</td>
                        <td>${persons[i]['name']}</td>
                        <td>${persons[i]['email']}</td>
                        <td>${persons[i]['gender']}</td>
                        <td>${persons[i]['age']+" Years"}</td>
                        <td><button class="btn btn-primary" onclick="editPerson(event)">Edit</button></td>
                        <td><button class="btn btn-danger" onclick="deletePerson(event)">Delete</button></td>   
                     </tr>`
        }

     tbody.innerHTML=data;
    }

}

function editPerson(e){
   form.classList.add('active');
   httpm="PUT"
   id= e.target.parentElement.parentElement.id;

  let selectedPerson = persons.filter((m)=>{return m['id'] ==id})[0];
  personEmail.value= selectedPerson.email;
  personName.value = selectedPerson.name;
  personAge.value = selectedPerson.age;
  personGender.value = selectedPerson.gender;


   

}

function deletePerson(e){
    id= e.target.parentElement.parentElement.id;
     fetch(url+"/"+id, {method:'DELETE'})
     .then(
        ()=>{
            getPersons();
        }
     )

}

