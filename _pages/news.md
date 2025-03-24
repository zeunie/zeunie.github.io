---
layout: archive
title: "News"
permalink: /news/
author_profile: true
---

<ul>
  {% assign news_items = site.news | sort: "date" | reverse %}
  {% for item in news_items %}
    <li>
      <strong>{{ item.date | date: "%b %Y" }}</strong> — {{item.title}} {{item.icon}}
    </li>
  {% endfor %}
</ul>
