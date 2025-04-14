# Workshop Introduction: Drawing Fonts with Pens in DrawBot 🖋️

Welcome to the **Font Pens in DrawBot** workshop!

In this session, we’ll explore how to draw letterforms programmatically using custom pens in [DrawBot](https://drawbot.com/). Pens are a key concept in font design, used to describe and manipulate the outlines of glyphs. They allow you to write functions that respond to drawing commands like `moveTo`, `lineTo`, and `curveTo`, giving you low-level control over the way letterforms are constructed.

We'll be working in Python inside DrawBot, focusing on understanding and writing our own pens, and how to iterate over and manipulate glyph data using simple Python concepts.

---

## 🖊️ Font Pens

At the heart of this workshop are the basic drawing commands used by pens:

- `moveTo(point)`: Starts a new subpath at the given point.
- `lineTo(point)`: Draws a straight line from the current point to the given point.
- `curveTo(handle1, handle2, endPoint)`: Draws a cubic Bézier curve using two handles and an endpoint.
- `qCurveTo(...)`: This is used for quadratic curves, but we’ll skip it for now to keep things focused.

We’ll write pens that respond to these commands and explore how different types of pens can be used to transform, decorate, or analyze outlines.

---

## 🔄 Iteration & Objects in Python

Before we dive into drawing, we’ll warm up with a small task that will help us think in terms of **data structures**—a skill that's essential when working with glyphs and outlines.

### **Task:**
Look around the room and pick an object. Now try to describe it using Python data structures:
- Use **lists** to represent collections of things (e.g., parts of the object).
- Use **dictionaries** to describe properties (e.g., color, size, material).

Example:

```python
mug = {
    "type": "ceramic",
    "color": "blue",
    "volume_ml": 300,
    "parts": ["handle", "body", "rim"]
}