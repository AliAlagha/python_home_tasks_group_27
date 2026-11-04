# AI-Powered Waste Sorting and Recycling Assistant

## Presentation Link

Video: _add link here_

## Team Overview

| Member | Student ID | Subsystem |
|---|---|---|
| Amirhossein Owji | 7227410 | AI waste classification |
| Mahshid Jafari | 7227434 | Recycling recommendations |
| Ali Alagha | 7226045 | History and statistics, User interface and integration |

## How to Start

Plain Python 3.11 or newer, no packages needed.

```bash
python -m stream_processing.main
```

## Class Diagram

```mermaid
classDiagram
    class Processor {
        <<abstract>>
        +process(item: dict) dict*
        +__add__(other: Processor) Pipeline
        +__or__(other: Processor) Pipeline
        +run(stream: iterable) generator
    }
    class ConfidenceFilter {
        +min_confidence : float
        +__init__(min_confidence: float)
        +process(item: dict) dict
    }
    class MaterialTransformer {
        +process(item: dict) dict
    }
    class RouteTransformer {
        +process(item: dict) dict
    }
    class Pipeline {
        +steps : list
        +__init__(steps: list)
        +process(item: dict) dict
        +__add__(other: Processor) Pipeline
    }
    class SensorStream {
        +items : list
        +index : int
        +__init__(items: list)
        +__iter__() SensorStream
        +__next__() dict
    }
    class sensor_stream {
        <<utility>>
        +camera(count: int) generator
    }
    Processor <|-- ConfidenceFilter
    Processor <|-- MaterialTransformer
    Processor <|-- RouteTransformer
    Processor <|-- Pipeline
    Pipeline "1" o-- "1..*" Processor : steps
    Processor ..> SensorStream : reads
    Processor ..> sensor_stream : reads camera()
```
