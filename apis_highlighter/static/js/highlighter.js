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
      annotationdata.project_id = highlight_text.dataset.project_id;
      annotationdata.orig_string = selection.toString();
      annotationdata.start = start;
      annotationdata.end = end;
      console.log(JSON.stringify(annotationdata));

      // add a helper span around the selection,
      // so that we can bind the popover to something
      var newel = document.createElement('span');
      newel.classList.add("highlighter-tmp");
      newel.classList.add("text-danger");
      selection.getRangeAt(0).surroundContents(newel);
      $(newel).popover({content: selection_menu(annotationdata, highlight_text), html: true});
      $(newel).popover("show");
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

function cleanup() {
  console.log("cleanup");
  document.querySelectorAll(".highlighter-tmp").forEach(element => {
    element.replaceWith(element.innerHTML);
  });
  document.querySelectorAll(".popover").forEach(element => {
    $(element).popover('dispose');
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

function selection_menu(annotationdata, textelement) {
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

function annotation_menu(element) {
  console.log(element);
  var menu = document.createElement("div");
  menu.classList.add("highlighter-annotation-menu");
  var dela = document.createElement("a");
  dela.href = element.dataset.delete +"?to=" + window.location.pathname + window.location.search;
  dela.innerHTML = "Delete";
  menu.appendChild(dela);
  $(element).popover({content: menu, html: true});
  $(element).popover("show");
}
