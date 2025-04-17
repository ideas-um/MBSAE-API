# CHANGELOG

Copyright (c) 2025 The Regents of the University of Michigan, IDEAS Lab

***************

# Version 0.0.0

Released 24 Mar 2025

## Added

- Initial code release

# Version 0.0.1

Released 28 Mar 2025

## Added

- Part Properties and Association relations may now exist in the system model and won't be written to an ADH (or conflict with updating the system model from an ADH)
- Instead of requiring a data structure for requirement text ("name", "description", "value:value", "value:units"), a requirement may also be represented as a single string, denoted by the "text" key-value pair.

## Changed

- In ReadADH, Part Properties are created for all blocks that are one-level below an existing block. This was to better facilitate the generation of Instance Specifications.

# Version 0.0.2

Released 17 Apr 2025

## Fixed

- Bug fixes in WriteInstance: (1) Boolean values can now be written from an Instance Specification to the ADH; (2) fixed issue associated with writing a scalar value after an array is written.
