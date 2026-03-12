const questions = [

{
question:"Which is the largest animal in the world?",
answers:[
{text:"Elephant",correct:false},
{text:"Blue Whale",correct:true},
{text:"Shark",correct:false},
{text:"Giraffe",correct:false}
]
},

{
question:"What does HTML stand for?",
answers:[
{text:"HyperText Markup Language",correct:true},
{text:"HighText Machine Language",correct:false},
{text:"HyperTool Markup Language",correct:false},
{text:"HighText Mark Language",correct:false}
]
},

{
question:"Which symbol is used for comments in JavaScript?",
answers:[
{text:"//",correct:true},
{text:"#",correct:false},
{text:"<!-- -->",correct:false},
{text:"/* */",correct:false}
]
},

{
question:"Which CSS property changes text color?",
answers:[
{text:"font-color",correct:false},
{text:"text-style",correct:false},
{text:"color",correct:true},
{text:"text-color",correct:false}
]
}

]

const questionElement=document.getElementById("question")
const answerButtons=document.getElementById("answer-buttons")
const nextButton=document.getElementById("next-btn")
const progressBar=document.getElementById("progress-bar")

let currentQuestionIndex=0
let score=0

function startQuiz(){
currentQuestionIndex=0
score=0
nextButton.innerHTML="Next"
showQuestion()
}

function showQuestion(){

resetState()

let currentQuestion=questions[currentQuestionIndex]

questionElement.innerHTML=(currentQuestionIndex+1)+". "+currentQuestion.question

progressBar.style.width=((currentQuestionIndex)/questions.length)*100+"%"

currentQuestion.answers.forEach(answer=>{

const button=document.createElement("button")

button.innerHTML=answer.text
button.classList.add("btn")

answerButtons.appendChild(button)

if(answer.correct){
button.dataset.correct=answer.correct
}

button.addEventListener("click",selectAnswer)

})

}

function resetState(){

nextButton.style.display="none"

while(answerButtons.firstChild){
answerButtons.removeChild(answerButtons.firstChild)
}

}

function selectAnswer(e){

const selectedBtn=e.target

const isCorrect=selectedBtn.dataset.correct==="true"

if(isCorrect){

selectedBtn.classList.add("correct")
score++

}else{

selectedBtn.classList.add("incorrect")

}

Array.from(answerButtons.children).forEach(button=>{

if(button.dataset.correct==="true"){
button.classList.add("correct")
}

button.disabled=true

})

nextButton.style.display="block"

}

function showScore(){

resetState()

questionElement.innerHTML=`🎉 Your Score: ${score} / ${questions.length}`

nextButton.innerHTML="Play Again"

nextButton.style.display="block"

progressBar.style.width="100%"

}

function handleNextButton(){

currentQuestionIndex++

if(currentQuestionIndex<questions.length){
showQuestion()
}else{
showScore()
}

}

nextButton.addEventListener("click",()=>{

if(currentQuestionIndex<questions.length){
handleNextButton()
}else{
startQuiz()
}

})

startQuiz()