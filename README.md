## 构建文档
[API documentation](./doc/_build/html/index.html)
```shell
# requirements
pip install sphinx
pip install sphinx_rtd_theme
```

```shell
# python_itican/
 sphinx-apidoc -M -F -o doc  .\iticanwrapper
```

```python
# edit python_itican/doc/conf.py

# add contents ahead .py file

import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# change file tail
html_theme = 'sphinx_rtd_theme'
```

```shell
# /python_itican/doc
./make html
```

## 使用流程

![](./usage_flow.jpg)

## <span id="PRESET_BAUD_TABLE">USBCAN 预设波特率表</span>

`can clock frequence = 80Mhz`

- 仲裁段波特率

| baudrate | brp | ts1 | ts2 | sample point |
| :------: | :-: | :-: | :-: | :----------: |
|  33.3k   | 60  | 34  |  5  |     87.5     |
|   50k    | 40  | 34  |  5  |     87.5     |
|  62.5k   | 20  | 55  |  8  |     87.5     |
|  83.3k   | 20  | 41  |  6  |     87.5     |
|   100k   | 20  | 34  |  5  |     87.5     |
|   125k   | 10  | 55  |  8  |     87.5     |
|   250k   |  8  | 34  |  5  |     87.5     |
|   500k   |  4  | 34  |  5  |     87.5     |
|   800k   |  2  | 39  | 10  |      80      |
|    1M    |  2  | 34  |  5  |     87.5     |


- 数据段波特率

| baudrate | brp | sjw | ts1 | ts2 | tdco | sample point |
| :------: | :-: | :-: | :-: | :-: | :--: | :----------: |
|   200k   | 20  |  0  | 15  |  4  |  0   |      80      |
|   250k   | 16  |  0  | 15  |  4  |  0   |      80      |
|   400k   | 10  |  0  | 15  |  4  |  0   |      80      |
|   500k   |  8  |  0  | 15  |  4  |  0   |      80      |
|   800k   |  4  |  0  | 19  |  5  |  0   |      80      |
|    1M    |  4  |  4  | 15  |  4  |  0   |      80      |
|  1.25M   |  4  |  4  | 11  |  4  |  24  |      75      |
|   1.6M   |  2  |  4  | 19  |  5  |  16  |      80      |
|    2M    |  2  |  4  | 15  |  4  |  16  |      80      |
|   2.5M   |  2  |  4  | 11  |  4  |  12  |      75      |
|    4M    |  2  |  2  |  7  |  2  |  8   |      80      |
|    5M    |  2  |  2  |  5  |  2  |  6   |      75      |
