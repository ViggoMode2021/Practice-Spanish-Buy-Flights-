
$(document).ready(function() {
start(questionNumber);

$(".submit-answer").on("click", function(event) {

    var userAnswer = parseInt($(this).attr("id"));
    answerCheck(userAnswer);

    setTimeout(function() {
                $(".submit-answer").removeClass("correctStyle incorrectStyle");
                 start(questionNumber);
             }, 1500)

     questionNumber++;
  });

});

var questionNumber = 0,
    totalCorrect = 0,
    optionFinal = 0;

var allQuestions = [
     {
        question: 'Who said, "My real father lost his head at Kings Landing. I made a choice, and I chose wrong."',
        choices: ["Robb Stark", "Jon Snow", "Theon Greyjoy", "Arya Stark"],
        answer: 2}
    ,{
        question: "What does Valar Morghulis mean?",
        choices: ["All men must die", "What is dead may never die", "Never say never", "All men must first live"],
        answer: 0}
    ,{
        question: "Which GOT character played Hermoine Granger's mom in Harry Potter?",
        choices: ["Melisandre", "Catelyn Stark", "Cersei Lannister", "Alerie Tyrell"],
        answer: 1}
    ,{
        question: 'Who said, "You knelt as boys, now rise as men of the Nights Watch."?',
        choices: ["Maester Aemon", "Eddard Stark", "Jeor Mormont", "Alliser Thorne"],
        answer: 2}
    ,{
        question: "What is Daenerys Targaryens brothers name?",
        choices: ["Varys", "Viserys", "Aerys", "Aegon"],
        answer: 1}
    ,{
        question: "What is a big fear of the Dothraki?",
        choices: ["Fire", "Salt water", "Heavy stone", "Crows"],
        answer: 1}
    ,{
        question: "How many swords make up the Iron Throne?",
        choices: ["500", "1000", "2000", "5000"],
        answer: 1}
    ,{
        question: "What were Jon Arryn's final words?",
        choices: ["Winter is coming", "Beware of the white walkers", "The seed is strong", "Beware the dwarf"],
        answer: 2}
    ,{
        question: "Who built the Iron Throne?",
        choices: ["Aerys the Mad King", "Aegon The Unlikely", "Aegon the Conqueror", "Aegon the Destroyer"],
        answer: 2}
    ,{
        question: "Which knight takes a lance through the neck while jousting?",
        choices: ["Ser Hugh of the Vale", "Ser Barristan Selmy", "Ser Ilyn Payne", "Ser Gregor Clegane"],
        answer: 0}
  ];

var result = [
    {
      image: "http://reactiongifs.me/wp-content/uploads/2014/10/tyrion-lannister-eyebrows-game-of-thrones.gif",
      comment: " Wowzers!"}
    ,{
      image: "http://www.reactiongifs.us/wp-content/uploads/2013/03/GoT_joffrey_approves.gif",
      comment:  " Not bad."}
    ,{
      image: "http://imagesmtv-a.akamaihd.net/uri/mgid:file:http:shared:mtv.com/news/wp-content/uploads/2015/04/eyeroll-1429202565.gif",
      comment: " You disappoint me child."}
    ,{
      image: "http://imagesmtv-a.akamaihd.net/uri/mgid:file:http:shared:mtv.com/news/wp-content/uploads/2015/06/seeaspider-1433860136.gif",
      comment: " Valar Morghulis."}
    ];


// continue with next question or end
var start = function(questionNumber) {
      $('h2').hide().fadeIn(400);

      if(questionNumber !== allQuestions.length){
          question(questionNumber);
      }else{
          end();
      }
};

// show question and possible answers
function question(questionNum) {
      $("h2").text(allQuestions[questionNum].question);

      $.each(allQuestions[questionNum].choices, function(i, answers){
         $("#" + i).html(answers);
      });
};

function end() {
  finalImage();
  $("ul").hide();
  $("h2").text("You scored " + totalCorrect + " out of " + allQuestions.length + ". " + result[optionFinal].comment);
  $("#image").html('<img src=' + result[optionFinal].image + ' alt="">').fadeIn(1000);
  $("#try-again-container").show();
  restart();
};

// result image accourding to correct answers
function finalImage() {
  if(totalCorrect < allQuestions.length && totalCorrect >= (allQuestions.length*.7)){
            optionFinal = 1;
    }else if(totalCorrect <= (allQuestions.length*.6) && totalCorrect >= (allQuestions.length*.2)){
          optionFinal = 2;
    }else if(totalCorrect !== allQuestions.length){
          optionFinal = 3;
    }
}

function restart(){
  $("#try-again").click(function(){
    questionNumber = 0,
    totalCorrect = 0,
    optionFinal = 0;

    start(questionNumber);
    $("#image").hide();
    $("#try-again-container").hide();
    $("ul").fadeIn(400);
  });
}

function answerCheck(userAnswer) {
     var correctAnswer = allQuestions[questionNumber].answer;

     if (userAnswer === correctAnswer) {
         $("#" + userAnswer).addClass("correctStyle");
         totalCorrect++;
     }else{
        $("#" + userAnswer).addClass("incorrectStyle");
     }
};
