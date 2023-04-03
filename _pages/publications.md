---
layout: page
permalink: /publications/
title: publications
description: I hope this page gets more crowded along the way...
years: [2023, 2021]

nav: true
nav_order: 1
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
