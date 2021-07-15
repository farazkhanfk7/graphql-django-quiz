# Queries Example

> To get quiz, quiz and answer for particular ID
```
{
  allQuiz(id:1){
    id
    title
    category {
      id
      name
    }
    question{
      title
    }
  }
  allQuestion(id:1){
    title
  }
  allAnswer(id:1){
    answerText
    isRight
  }
}

```
<br>

> Mutation to create new Category ( No foreign key relation )
```
mutation firstmutation{
  addCategory(name:"blockchain"){
    category{
      id
      name
    }
  }
}
```
<br>

> Mutation to create Quiz ( with foreign key : category )
```
mutation secondmutation{
  addQuiz(title:"Blockchain Quiz",category:4){
    quiz{
      title
      category{
        id
        name
      }
    }
  }
}
```
<br>

> Mutation to update existing category ( IoT -> Blockchain )
```
mutation firstmutation{
  addCategory(name:"blockchain",id_:4){
    category{
      id
      name
    }
  }
}
```