// 获取 gpt 数据
async function get_eatgpt() {
  const typingArea = document.getElementById("food");
  let loading_div = document.createElement("dev");
  loading_div.classList.add('flow-text', 'element', 'animate__animated', 'animate__wobble');
  load_text = document.createTextNode('GPT 正在整理菜单...');
  loading_div.appendChild(load_text);
  typingArea.appendChild(loading_div);

  const result = await fetch('/get_eatgpt');
  const food_meta = await result.json();
  const food_name = Object.keys(food_meta);
  const food_info = Object.values(food_meta);
  
  const intervalTime = 300;

  typingArea.removeChild(loading_div)
  for (i=0; i < food_name.length; i++){
    let food_div = document.createElement("dev");

    let food_key = food_name[i];
    let food_value = food_info[i];
    let food_li = document.createElement("p");
    let food_herf = document.createElement("a");
    food_herf.href = 'https://search.bilibili.com/all?keyword=' + food_key;
    food_herf.classList.add('accent-4', 'element', 'animate__animated', 'animate__bounceInUp');
    food_herf.target = '_blank';
    food_li.classList.add('accent-4', 'element', 'animate__animated', 'animate__bounceInUp');
    let line_break = document.createElement("br");
    let line_break2 = document.createElement("br");
    let line_break3 = document.createElement("br");

    let food_split = document.createTextNode('·······························································································································');

    let food_name_text = document.createTextNode(food_key);
    let food_info_text = document.createTextNode(food_value);
    food_herf.appendChild(line_break3);
    food_herf.appendChild(food_name_text);
    food_herf.appendChild(line_break);
    food_li.appendChild(food_herf);
    food_li.appendChild(food_split);
    food_li.appendChild(line_break2);
    food_li.appendChild(food_info_text)
    typingArea.appendChild(food_li);

  }
}

get_eatgpt()



// 解析
