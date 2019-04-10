## Описание json файла с информацией для предварительного заполнения базы данных.

При обработке файла рассматриваются следующие поля:
1. DocumentSupertype - список со строками описывающих названия типов документов
2. AnalyzerType - список со строками описывающий названия типов анализа применяемых в системе
3. PropertyType - список со строками описывающий названия типов свойств используемых в системе
4. Organisation - название организации которое будет добавлено
5. DataSource - список источников документов, каждый элемент должен содержать поля source_link(ссылка на интернет ресурс) и crawler_name(название сборщика для этого ресурса)
6. Analyzer - список анализаторов доступных в системе, каждый элемент должен содержать поял analyzer_type(тип анализа который предоставляет этот анализатор, этот тип должен быть добавлен в систему ранее или в этой сессии обнавления базы данных), version(версия анализатора) и name(название анализатора)

пример:
```
{
  "DocumentSupertype": ["document-type-example"],
  "AnalyzerType": ["analyze-type-example"],
  "PropertyType": ["property-example"],
  "Analyzer": [
    {
      "name": "cool-analyztor-name",
      "version": 1,
      "analyzer_type": "analyze-type-example"
    }
  ],
  "DataSource": [
    {
      "source_link": "http://www.cool-link.net",
      "crawler_name": "cool-scanner"
    }
  ],
  "Organisation": "cool-organisation"
}