highlighttexts = document.querySelectorAll(".highlight-text");
highlighttexts.forEach(text => {
  // we are adding the event listeners to the parents of the
  // .highlight-text divs, because the divs are being replaced
  // during during operation and with the replacement the
  // eventListeners will be gone, too.
  parentn = text.parentNode;
  parentn.addEventListener("pointerup", function(event) {
    selection = document.getSelection();
    if (selection.getRangeAt(0).cloneContents().querySelectorAll("mark").length > 0) {
      console.log("Already contains mark");
      return;
    }
    highlight_text = selection.anchorNode.parentElement.closest(".highlight-text");
    if (!selection.isCollapsed && highlight_text) {

      // this block is copied from the original highlighter
      // does the trick, not sure how
      range = window.getSelection().getRangeAt(0);
      priorRange = range.cloneRange();
      priorRange.selectNodeContents(highlight_text);
      priorRange.setEnd(range.startContainer, range.startOffset);
      shadow_selection = priorRange.cloneContents();
      console.log(shadow_selection);
      const num_brs = shadow_selection.querySelectorAll("br").length;
      start = priorRange.toString().length + num_brs;
      end = start + range.toString().length;

      var annotationdata = {};
      annotationdata.text_object_id = highlight_text.dataset.text_object_id;
      annotationdata.text_content_type_id = highlight_text.dataset.text_content_type_id;
      annotationdata.text_field_name = highlight_text.dataset.text_field_name;
      annotationdata.project_id = highlight_text.dataset.project_id;
      annotationdata.orig_string = selection.toString();
      annotationdata.start = start;
      annotationdata.end = end;
      console.log(JSON.stringify(annotationdata));

      // add a helper span around the selection,
      // so that we can bind the popover to something
      selspan = document.getElementById("highlightermarker").cloneNode(true);
      selspan.classList.add("selection-span");
      selection.getRangeAt(0).surroundContents(selspan);

      popup = create_popup_near_element(selspan);

      popup.appendChild(selection_menu(annotationdata, highlight_text));
      makemovable(popup);
    }
  });

  parentn.addEventListener("pointerdown", function(event) {
    cleanup();
  });

});

// this overrides the EntityRelationForm_response from the apis core
// codebase, so that we can add a eventlistener that reloads the text
var native_EntityRelationForm_response = EntityRelationForm_response;
EntityRelationForm_response = function(response) {
  console.log("override EntityRelationForm_response");
  native_EntityRelationForm_response(response);
  if (response.test) {
    evt = new Event("formresponse");
    document.dispatchEvent(evt);
  }
}

function create_popup_near_element(element) {
  rect = element.getBoundingClientRect();

  popup = document.getElementById("highlighterpopup").cloneNode(true);
  popup.classList.add("highlighter-popup");
  document.body.appendChild(popup);
  popup.style.display = "block";
  poprect = popup.getBoundingClientRect();
  popup.style.top = rect.top + rect.height + window.scrollY + 10 + 'px';
  popup.style.left = (rect.left + window.scrollX - (poprect.width / 2)) + 'px';
  if (getCookie("highlighter_menu_top")) {
    popup.style.top = getCookie("highlighter_menu_top");
  }
  if (getCookie("highlighter_menu_left")) {
    popup.style.left = getCookie("highlighter_menu_left");
  }
  return popup;
}

function cleanup() {
  document.querySelectorAll(".selection-span").forEach(element => {
    element.replaceWith(element.innerHTML);
  });
  document.querySelectorAll(".highlighter-popup").forEach(element => {
    element.remove();
  });
}

function replace_with_data_source(element) {
  fetch(element.dataset.source)
    .then((response) => response.text())
    .then((text) => {
       element.outerHTML = text;
    });
}

function selection_menu(annotationdata, textelement) {
  var menu = document.getElementById("highlightermenu").cloneNode(true);
  menu.classList.add("highlighter-menu");
  menu.style.display = "block";
  menu.querySelectorAll(".highlighter-menu-item").forEach(element => {
    element.onclick = function() {
      form = document.getElementById("form_triple_form_" + this.dataset.rel).cloneNode(true);
      var input = document.getElementById("hiddeninput").cloneNode(true);
      input.setAttribute("value", JSON.stringify(annotationdata));
      form.appendChild(input);
      form.action = "/highlighter" + form.getAttribute("action").trim();
      document.addEventListener("formresponse", function(event) {
          cleanup();
          replace_with_data_source(textelement);
      }, { once: true });
      menu.innerHTML = '<h3>' + this.innerHTML + '</h3>';
      menu.appendChild(form);
    };
  });
  return menu;
}

function annotation_menu(element) {
  popup = create_popup_near_element(element);
  popup.style.width = "300px";
  var menu = document.getElementById("highlighter-annotation-menu").cloneNode(true);
  menu.classList.add("highlighter-annotation-menu");
  menu.style.display = "block";
  popup.append(menu);
  header = document.querySelector('.highlighter-annotation-menu #header')
  header.innerHTML = element.title.replace("<", "&lt");
  dela = document.querySelector('.highlighter-annotation-menu #delbtn');
  dela.href = element.dataset.delete +"?to=" + window.location.pathname + window.location.search;
  makemovable(popup);
}

// this is copied from: https://phuoc.ng/collection/html-dom/make-a-draggable-element/
function makemovable(ele) {
  // The current position of mouse
  let x = 0;
  let y = 0;
  
  // Handle the mousedown event
  // that's triggered when user drags the element
  const mouseDownHandler = function (e) {
      // Get the current mouse position
      x = e.clientX;
      y = e.clientY;
  
      // Attach the listeners to `document`
      document.addEventListener('mousemove', mouseMoveHandler);
      document.addEventListener('mouseup', mouseUpHandler);
  };
  
  const mouseMoveHandler = function (e) {
      // How far the mouse has been moved
      const dx = e.clientX - x;
      const dy = e.clientY - y;
  
      // Set the position of element
      ele.style.top = `${ele.offsetTop + dy}px`;
      ele.style.left = `${ele.offsetLeft + dx}px`;
      setCookie("highlighter_menu_top", ele.style.top, 365);
      setCookie("highlighter_menu_left", ele.style.left, 365);
  
      // Reassign the position of mouse
      x = e.clientX;
      y = e.clientY;
  };
  
  const mouseUpHandler = function () {
      // Remove the handlers of `mousemove` and `mouseup`
      document.removeEventListener('mousemove', mouseMoveHandler);
      document.removeEventListener('mouseup', mouseUpHandler);
  };
  
  ele.addEventListener('mousedown', mouseDownHandler);
} 

// from https://www.w3schools.com/js/js_cookies.asp
// returning `false` instead of empty string
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return false;
}

// from https://www.w3schools.com/js/js_cookies.asp
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
