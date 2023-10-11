highlighttexts = document.querySelectorAll(".highlight-text");
highlighttexts.forEach(text => {
  text.addEventListener("pointerup", function(event) {
    selection = document.getSelection();
    if (!selection.isCollapsed) {
      var annotationdata = {};

      highlight_text = selection.anchorNode.parentElement.closest(".highlight-text");
      annotationdata.text_object_id = highlight_text.dataset.text_object_id;
      annotationdata.text_content_type_id = highlight_text.dataset.text_content_type_id;

      start = selection.anchorOffset - 3;
      length = selection.focusOffset - selection.anchorOffset;
      prevNode = selection.anchorNode.previousSibling;
      while (prevNode) {
        start = start + prevNode.textContent.length;
        prevNode = prevNode.previousSibling;
      }

      annotationdata.start = start;
      annotationdata.end = start + length;

      console.log(JSON.stringify(annotationdata));

      var newel = document.createElement('span');
      newel.classList.add("highlighter-tmp");
      newel.classList.add("text-danger");
      selection.getRangeAt(0).surroundContents(newel);
      $(newel).popover({content: menu(annotationdata, text), html: true});
      $(newel).popover("show");
    }
  });

  text.addEventListener("pointerdown", function(event) {
    cleanup();
  });

});

var native_EntityRelationForm_response = EntityRelationForm_response;
EntityRelationForm_response = function(response) {
  console.log("override EntityRelationForm_response");
  native_EntityRelationForm_response(response);
  if (response.test) {
    evt = new Event("formresponse");
    document.dispatchEvent(evt);
  }
}

function cleanup() {
  console.log("cleanup");
  document.querySelectorAll(".highlighter-tmp").forEach(element => {
    $(element).popover('dispose');
    element.replaceWith(element.innerHTML);
  });
}

function replace(element) {
  console.log("replace");
  fetch(element.dataset.source)
    .then((response) => response.text())
    .then((text) => {
       element.outerHTML = text;
    });
}

function menu(annotationdata, textelement) {
  var menu = document.createElement("div");
  menu.classList.add("highlighter-menu");
  // this should definitly not be hardcoded
  var reltypes = ["person_to_place", "person_to_institution", "person_to_person"];
  reltypes.forEach(function (item, index) {
    var div = document.createElement("div");
    div.innerHTML = item;
    div.onclick = function () {
      form = document.getElementById("form_triple_form_" + item).cloneNode(true);
      var input = document.createElement("input");
      input.setAttribute("type", "hidden");
      input.setAttribute("name", "annotationdata");
      input.setAttribute("value", JSON.stringify(annotationdata));
      form.appendChild(input);
      form.action = "/highlighter" + form.getAttribute("action").trim();
      document.addEventListener("formresponse", function(event) {
          cleanup();
          replace(textelement);
      }, { once: true });
      menu.innerHTML = '<h3>' + item + '</h3>';
      menu.appendChild(form);
    };
    menu.appendChild(div);
  });
  return menu;
}
