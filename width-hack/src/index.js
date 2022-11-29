import { addNewChild, makeElement, style, makeHtmlDemo, makeFunctionalDemo, formatText } from "./util.js";

import awesomeDemo from "./functionalDemos/awesomeDemo.html";

import basicMarkup from "./htmlDemos/basicMarkup.html";
import basicMarkupFunctional from "./functionalDemos/basicMarkupFunctional.html";

import calcDemo from "./htmlDemos/calcDemo.html";
import calcDemoFunctional from "./functionalDemos/calcDemoFunctional.html";

import classDemo from "./htmlDemos/classDemo.html";
import classDemoCss from "./htmlDemos/classDemoCss.txt";
import inlineClassDemo from "./htmlDemos/inlineClassDemo.html";

import bareBones from "./htmlDemos/bareBones.html";
import bareBonesCss from "./htmlDemos/bareBonesCss.txt";
import bareBonesFunctional from "./functionalDemos/bareBonesFunctional.html";

import bareBonesSlightFunctional from "./functionalDemos/bareBonesSlightFunctional.html";

import bareBonesMultipleFunctional from "./functionalDemos/bareBonesMultipleFunctional.html";
import bareBonesMultiple from "./htmlDemos/bareBonesMultiple.html";

import singleGoodButtonFunctional from "./functionalDemos/singleGoodButtonFunctional.html";

import oneDimensionalFunctional from "./functionalDemos/oneDimensionalFunctional.html";

import blockerDivsFunctional from "./functionalDemos/blockerDivsFunctional.html";

import overflowCss from "./htmlDemos/overflowCss.txt";
import overflowFunctional from "./functionalDemos/overflowFunctional.html";

import oneDimensionalFinalFunctional from "./functionalDemos/oneDimensionalFinalFunctional.html";

import naive2D from "./htmlDemos/naive2D.html";
import naive2DCss from "./htmlDemos/naive2DCss.txt";

import naiveDemoFunctional from "./functionalDemos/naiveDemoFunctional.html";

import better2D from "./htmlDemos/better2D.html";
import verticalButtonsCss from "./htmlDemos/verticalButtonsCss.txt";

// WILL PROBABLY NEED TO REMOVE THIS EVENTUALLY //
document.body.style["background"] = "rgb(20, 20, 40)";

function addSpace() {
    addNewChild(currentElement, "div", {"height": "1em"});
}

function addHr() {
    addNewChild(currentElement, "hr", {"width": "calc(100% - 30px)", "align-self": "center"});
}

function addText(text) {
    addNewChild(currentElement, "p", {"margin": "0.6em 0"}, formatText(text));
}

function makeLinkString(text, link) {
    let element = makeElement("a", null, text);
    element.setAttribute("href", link);
    return element.outerHTML;
}

let externalContainer = addNewChild(document.body, "div", {"width": "500px", "margin": "auto"});

let mainContainer = addNewChild(externalContainer, "div", {"display": "flex", "align-items": "flex-start", "flex-direction": "column","width": "100%", "min-height": "500px", "background": "white", "font-family": "sans-serif", "text-indent": "1em", "line-height": "1.5", "margin": "auto", "padding": "8px"});
let currentElement = mainContainer;

addText("Hello! I've been seeing more and more posts using a trick that I've seen called \"<span style=\"color:steelblue;font-weight:bold\">width-hacking</span>\", so I thought it could be nice to have a post describing it in depth for reference, as well as to introduce it to people who don't know about it yet!");
addText("This post is aimed at people who know at least the basics of css, but don't really know how to make interactive posts with cohost's restrictions in particular.");
addText("This post has unfortunately reached \"blog post\" length, so you might have to settle in if you're planning to read through the whole thing. Alternatively, you could skim through this post over the course of about one minute and play around with the demos. That's probably what I would do.")

addHr();

addText("In this post I'll build up from one simple but clever technique to show you how to make the following demo, which emulates 2d grid movement:");

currentElement.appendChild(makeFunctionalDemo(awesomeDemo, true));

addText("The goal of this post is not only to show you \"how to make grid movement in cohost\", but also to give a demonstration of how width-hacking works. Grid movement happens to be an illustrative example of width-hacking, but you can do so, so much more with it.");

addText("With width-hacking, you'll find that something like the demonstration above can be even be written by hand (indeed, this demo was handwritten), so imagine how powerful this technique can be if we generate HTML programatically! Let's get into it!");

addHr();

addText("Consider the following basic markup structure:");

currentElement.appendChild(makeHtmlDemo(basicMarkup));
addSpace();
currentElement.appendChild(makeFunctionalDemo(basicMarkupFunctional));

addText("Sibling relationships of HTML elements like the one between span1 and span2 are common, but it is difficult to make these two elements \"communicate\" with the tools we have in cohost's toolbox.");
addText("If we put more words inside of span1 to increase its width, span2 will move to the right to accomodate the new dimensions of span1, but that's about the extent of what we can do to make span1 influence span2. Even worse, there are probably very few things we can do to span2 that will cause span1 to change because it comes after span1.");

addText("The main tools we have besides \"elements pushing each other around\" that cause interesting interactions are <b>&lt;details&gt; tags</b> and css' <b>calc()</b> function. I'm not going explain the basics of &lt;details&gt; tags so you should read <a href='https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details'>the mdn web docs page on them</a> if you're unfamiliar because we'll be relying on them heavily later. To see how to use calc(), I've changed the style of span1 in the following example:");

currentElement.appendChild(makeHtmlDemo(calcDemo));
addSpace();
currentElement.appendChild(makeFunctionalDemo(calcDemoFunctional));

addText("We need to set the \"display\" of span1 to \"inline-block\" because the \"width\" property is ignored for elements with \"display: inline\", which &lt;span&gt;s have by default. Then, we set the width of span1 to calc(50% + 20px). Here, 50% refers to the width of span1's parent container, which is the &lt;div&gt; with a width of 300px. All together, this means that the width of span1 becomes 0.5 * 300px + 20px which ends up being 170px.");

addText("This example may not seem particularly exciting, but calc() completely blows the door open for us by allowing us to have two &lt;details&gt; tags interact with each other, as well as other elements, even if neither of them contains the other. Let's see how with a more complicated example.");

addHr();

addText("Because inline styling of elements becomes unwieldy very quickly, I am going to use css class syntax for readability in the rest of these examples. Please recognize, however, that everything is implemented with inline styling.");

addText("As an example, I may write something like the following in a demonstration:")

currentElement.appendChild(makeHtmlDemo(classDemo));
addSpace();
currentElement.appendChild(makeHtmlDemo(classDemoCss));

addText("But if you were to put this markup in a chost, it would need to be implemented as follows:");

currentElement.appendChild(makeHtmlDemo(inlineClassDemo));

addText("Hopefully you agree that the first way is more readable! Now, to begin making the demo I showed at the beginning, let's just focus on making 1-dimensional moment for now. We'll start really simple, placing only the following elements:");

currentElement = addNewChild(currentElement, "ul", {"text-indent": "0"});
addNewChild(currentElement, "li", null, formatText("A div that I'll refer to as !memory. This div serves as the \"main screen\" for the game, and we'll see why I call it memory later."));
addNewChild(currentElement, "li", null, formatText("A div that I'll refer to as the !hero. This div is a child of !memory and has its background set to the eggbug image that the user will be able to move around."));
addNewChild(currentElement, "li", null, formatText("An unstyled details tag. It has as children a &lt;summary&gt; tag positioned absolutely near the bottom of the screen (this is what the user clicks on to open the details element, so I'll call it !button), as well as a &lt;div&gt; with its width set to 1px which I'll call \"oneWide.\""));

currentElement = mainContainer;
currentElement.appendChild(makeHtmlDemo(bareBones));
addSpace();
currentElement.appendChild(makeHtmlDemo(bareBonesCss));

addText("This produces the following:");
currentElement.appendChild(makeFunctionalDemo(bareBonesFunctional, true));

addText("Most of this styling is just to position the elements and specify their dimensions, but I'll go over the styling that is a bit more subtle.");

currentElement = addNewChild(currentElement, "ul", {"text-indent": "0"});
addNewChild(currentElement, "li", null, formatText("Setting \"display: inline-flex\" on !memory essentially means that it will only be as wide and tall as it needs to be to fit its contents that are not absolutely positioned. Since !hero is absolutely positioned and the &lt;details&gt; has width and height equal to 0 by default, this means that the width and height of !memory are both 0."));
let details = addNewChild(currentElement, "details", {"cursor": "pointer"});
addNewChild(details, "summary", {"margin-left": "20px"}, formatText('<span style="font-weight:bold">"What do you mean !memory has a width and height of 0? I clearly see !memory right there. It\'s that gigantic turquoise rectangle."</span>'));
addNewChild(details, "div", {"margin-left": "20px", "cursor": "auto"}, formatText('Here, width and height refer to the content of !memory. Sometimes when I talk about the width and height of an element, I\'ll be referring to its contents, and sometimes I\'ll be referring to the container overall. I\'ll try to be unambiguous in my wording but it\'s something you will have to pay attention to. The turquoise rectangle you see is because !memory has its \"padding-right\" set to 160px and its \"padding-bottom\" set to 120px. If you inspect !memory with your browser\'s dev tools, you\'ll see that indeed it has a width of 0 and a height of 0.'));
details = addNewChild(details, "details", {"margin-left": "20px", "cursor": "pointer"});
addNewChild(details, "summary", {"font-weight": "bold"}, "Here's what that looks like in Chrome's dev tools");
let img = addNewChild(details, "img", {"border-radius": "8px", "cursor": "auto"});
img.setAttribute("src", "https://staging.cohostcdn.org/attachment/37ba3919-fdd1-4d4c-a870-81b667b503f5/memory.png");
addNewChild(currentElement, "li", null, formatText("The other important bit of styling is setting \"position: relative\" on !memory and \"position: absolute\" on !hero and !button. Setting \"position: relative\" on !memory basically says to its children, \"Hey, if you have 'position: absolute', then if you set any of the properties 'top', 'left', 'bottom', or 'right', it will be relative to me!\". Therefore when we set \"left\" and \"top\" in !hero and !button, these positions are set relative to the top left corner of !memory."));

currentElement = mainContainer;
addText("Now I'm sure you've been clicking !button incessantly in the demo above. If you look closely, you'll see that !memory becomes 1 pixel wider when you open the details tag, and 1 pixel smaller when you close it. This is because of the oneWide element: when the details tag is open, its dimensions are as large as its non-absolute contents (this consists of only the oneWide element, so its dimensions become 1px by 0px). Then, !memory stretches to be as big as it needs to be to accommodate these new contents, also becoming 1px by 0px. This is in addition to the padding we set earlier.");

addText("Now we can finally make something interesting happen; I am going to make exactly one change to the demo above, changing \"left: 0\" to \"left: calc(40 * calc(100% - 160px))\" for !hero. I'll demystify that expression in a moment, but check out what happens when you click !button now.");

currentElement.appendChild(makeFunctionalDemo(bareBonesSlightFunctional, true));

addText("Let's break that down. By default, !memory is a container that has an overall width of 160px. Thus, when we compute \"calc(100% - 160px)\", this reduces to 160px - 160px, which is just 0. Further multiplying by 40 still gives 0, so the \"left\" property of !hero is 0 by default, just like before.");
addText("However, when the details tag is open, we know that this increases the overall width of !memory to 161px. Now computing \"calc(100% - 160px)\" reduces to 161px - 160px, which is 1px. But there is still more computation to do: calc(40 * 1px) finally reduces to 40px, so when the details tag is open, the \"left\" of !hero is set to 40px.");
addText("To summarize, setting \"left: calc(40 * calc(100% - 160px))\" on !hero essentially makes !hero say \"I will move 40px to the right every time I see the width of !memory increase by 1.\" I like to think of the width of the content of !memory as storing a \"variable\" that we can refer to from other elements, hence the name \"memory\". Every time you see the expression \"calc(100% - 160px)\", you should really read this as \"access the variable we have stored in !memory.\"");
addText("This setup makes it incredibly easy to move !hero multiple times: we just need to copy and paste our details tag repeatedly (and edit the positions of the summaries so that they aren't all in the same location). That's the only thing I've done to get to the following demo:");

currentElement.appendChild(makeFunctionalDemo(bareBonesMultipleFunctional, true));

addText("Here's the markup for it. The only styling that changed for the various buttons is their \"left\" property, just to make sure they're in distinct locations. Aside from that, everything is exactly the same as before.");

currentElement.appendChild(makeHtmlDemo(bareBonesMultiple));

addText("Every time you open a details tag in the above demo, you are making the content of !memory 1 pixel wider, and !hero is piggybacking off of that and moving 40 pixels to the right.");
addText("We have almost achieved 1-dimensional movement. The main thing that is missing is the fact that we want the user to always click in one location (right on the dpad) to move right, and in another location (left on the dpad) to move left. Currently, the user needs to remember which details tags are open and which are closed and click accordingly in order to move left or right, which is unintuitive and unwieldy.");
addText("To solve this problem, let's return to the case where we only had a single !button. At the beginning, we can place this !button at the right side of the dpad, because clicking there will open the details tag and move the !hero to the right. Then, to move left we want to click that same details tag, which should now be located at the left side of the dpad.")

currentElement.appendChild(makeFunctionalDemo(singleGoodButtonFunctional, true));

addText("If you've followed up to this point, you should know exactly how this was implemented. Just like how we wanted !hero to move 40px to the right every time we opened a details tag, we want !button to move 40px to the left every time we open a details tag. Thus, the only change that was required (besides adding in an element with the dpad image) was changing \"left\" for !button from \"90px\" to \"calc(90px - 40 * calc(100% - 160px))\".");
addText("Now we can add all of the other buttons back, making sure that they start to the right of the original button and move to the left by 40px every time a details tag is opened.");

currentElement.appendChild(makeFunctionalDemo(oneDimensionalFunctional, true));

addText("Something you may notice about this demo is that if you click the buttons out of order, the buttons on the dpad may no longer behave as desired, ie clicking right on the dpad may move the hero left instead of right (why?). It is imperative that the user is only able to click on buttons when they lie over the left or right of the dpad.");
addText("There is a simple solution to ensure this: simply place some giant blocker-divs covering everything except the dpad so that the player cannot click buttons unless they currently lie over the dpad. Here's what that might look like (in a final product we would make these invisible)");

currentElement.appendChild(makeFunctionalDemo(blockerDivsFunctional, true));

addText("There are many aesthetic changes we should probably make at this point. A very noticeable annoying behavior of this demo is that the width of the \"screen\" visibly changes by 1 pixel every time we move the !hero. We would like the screen to be a consistent 160px by 120px, so one way we can fix this is by wrapping the entire thing in a div with the following styling:");

currentElement.appendChild(makeHtmlDemo(overflowCss));

addText("This results in a cleaner, less \"shaky\", view of the previous demo:");

currentElement.appendChild(makeFunctionalDemo(overflowFunctional, true));

addText("From here, there are a few smaller tweaks we can make for a more pleasant experience. First, I suggest setting \"cursor\" to \"pointer\" on all of our buttons, so that the user knows when they can click on the dpad. We should also make all buttons and blocker divs invisible (I do this by removing the \"background\" property from all of them, but you can also play with the \"opacity\" property, or even just set the background to a completely transparent color). Last, I like to put a simple backdrop div behind the controller area to distinguish it from the rest of the screen. With that, we end up with the following gizmo!");

currentElement.appendChild(makeFunctionalDemo(oneDimensionalFinalFunctional, true));

addText("We are actually already very close to 2d movement, and you might see how we can make it already! We're effectively storing the x coordinate of !hero in the width of !memory, why not store the y coordinate of !hero in the height of !memory? Indeed, this is exactly what we do, but there is one small accommodation we must make.");
addText("If we naively try to add buttons which contribute to the height of !memory, maybe in a way similar to the following example:")

currentElement.appendChild(makeHtmlDemo(naive2D));
addSpace();
currentElement.appendChild(makeHtmlDemo(naive2DCss));

addText("We won't get the intended behavior.");

currentElement.appendChild(makeFunctionalDemo(naiveDemoFunctional, true));

addText("This is because !memory has \"flex-direction: row\" by default, meaning it will line up its contents horizontally as they are added. If we line up a bunch of 1px tall elements horizontally upon opening our vertical buttons, this will at most make the content of !memory 1px tall, when we would like it to vary up to 3px tall.");
addText("The solution is <em>not</em> to change \"flex-direction\" to \"column\" on !memory, as this would break our horizontal buttons. Instead, we just need to wrap our vertical buttons in a &lt;div&gt; inside of !memory with the following styling:");

currentElement.appendChild(makeHtmlDemo(better2D));
addSpace();
currentElement.appendChild(makeHtmlDemo(verticalButtonsCss));

addText("This essentially places another element that acts like a vertical version of !memory inside of !memory, which allows our vertical buttons to properly stack up their heights inside of !memory. After taking care to postion things correctly which is tedious but nothing new, we end up with the demo I showed you at the beginning of the post!");

currentElement.appendChild(makeFunctionalDemo(awesomeDemo, true));

addText("If you get the ball rolling with something like this and you don't hate your code yet, there's a ton of directions you can go. You can add \"collision\" with obstacles by having blocker-divs that move over the controls as the !hero moves. You can put things besides oneWides or oneTalls inside of details tags to allow the user to \"unlock\" new things upon reaching certain locations. If you can think of a turn based mechanic, I imagine you can implement it with a clever enough approach. You can probably even implement real-time mechanics with clever uses of animation!");

addText("Finally, " + makeLinkString("here", "https://gist.github.com/Corncycle/abe4afee3129c8fad7b54975e845edfd") + " is a link to the source HTML for the completed demo. It may be smaller than you think! I was surprised how compact it can be when I first started trying to make grid movement.");

addHr();

currentElement = addNewChild(currentElement, "div", {"text-indent": "0"});
addText("<strong>Here are some posts I've seen using width-hacking that show how you can use it to do much more than grid movement!</strong>")

addText("I learned about width-hacking by inspecting the source of  " + makeLinkString("this", "https://cohost.org/blackle/post/72096-h3-style-text-alig") + " charming post.");
addText("I have no fucking idea what is going on in " + makeLinkString("this", "https://cohost.org/blackle/post/260204-div-style-width-60") + " mindblowing post, but I can't imagine you could make something like it <em>without</em> width hacking.");
addText(makeLinkString("This", "https://cohost.org/jazzrabbit/post/386683-my-first-css-crime") + " is a fun port of Wordle, which includes a generator to make your own Wordles!");
addText(makeLinkString("Here", "https://cohost.org/cefqrn/post/457151-binary-to-decimal-ex") + " is another explanation of width-hacking, and how it was used to make a binary to decimal widget!");

addText("<strong>Now go make something awesome!</strong>");