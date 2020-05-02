function postData() {
  var text = document.getElementById("text").value;

  $.ajax({
    url: 'index.html',
    type: 'post',
    data: text,
    success: successGetJson });
}

function successGetJson(data) {
  var text_form = document.getElementById("text_form");

  document.body.style.backgroundColor = "#fff";

  data = eval(data);

  var p_content = document.createElement('P');
  p_content.id = 'p_content';

  for (i = 0; i < data.length; i++) {
    var s;
    if (data[i]['result'] === 'PERSON') {
      s = document.createElement('span');
      s.className = 'PERSON';
    } else {
      s = document.createElement('span');
      s.className = 'O';
    }
    s.setAttribute('title', data[i]['word'] + '\nP(PERSON) = ' + data[i]['prob'].toFixed(4) + '\nP(O) = ' + (1 - data[i]['prob']).toFixed(4));
    s.innerHTML = data[i]['word'] + ' ';
    p_content.appendChild(s);
  }
  text_form.parentNode.insertBefore(p_content, text_form.nextSibling)
  text_form.style.display = 'none';

  var btn_back = document.getElementById('btn_back');
  if (btn_back != null) {
    btn_back.style.display = 'block';
  } else {
    var btn_back = document.createElement('input');
    var header = document.getElementById('header');

    btn_back.type = 'button';
    btn_back.setAttribute('id', 'btn_back');
    btn_back.value = 'Back';
    header.appendChild(btn_back);
    btn_back.addEventListener('click', goBack);
  }
}

function goBack() {
  var btn_back = document.getElementById('btn_back');
  var p_content = document.getElementById('p_content');
  var text_form = document.getElementById("text_form");

  document.body.style.backgroundColor = "#f0f0f0";
  btn_back.style.display = 'none';
  p_content.remove()
  text_form.style.display = 'block';
}

var btn_submit = document.getElementById('text_submit');
btn_submit.addEventListener('click', postData);

