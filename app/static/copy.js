function copy(str){
  let tmp   = document.createElement('INPUT'),
      focus = document.activeElement;

  tmp.value = str;

  document.body.appendChild(tmp);
  tmp.select();
  document.execCommand('copy');
  document.body.removeChild(tmp);
  focus.focus();
}

document.addEventListener('DOMContentLoaded', e => {
  let input = document.querySelector('#input'),
      bCopy = document.querySelector('#bCopy'),
      log   = document.querySelector('#log');

var success_alert = '<div class="alert alert-success" role="alert" class="alert">';
success_alert += 'Ссылка успешно скопирована в буфер обмена, нажмите <a href="https://l4y.su" class="alert-link">сюда</a> если хотите создать еще одну ссылку.';
success_alert += '</div>';

var danger_alert = '<div class="alert alert-danger" role="alert" class="alert">';
danger_alert += 'Упс, скопируйте пожалуйста ссылку в ручную';
danger_alert += '</div>';


  bCopy.addEventListener('click', e => {
    if(input.value){
      try{
        copy(input.value);
        log.innerHTML = success_alert;
      }catch(e){
        log.innerHTML = danger_alert;
      }
    }
  });
});
