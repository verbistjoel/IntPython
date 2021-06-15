"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a
flag for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO.
Each has an approach datetime, a nominal approach distance, and a relative
approach velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object,
    such as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name=None, diameter=float('nan'),
                    hazardous=False, approaches=[]):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to
         the constructor.
        """
        self.designation = str(designation)

        if str(name) == '' or str(name) == 'None':   # make sure no empties
            self.name = None
        else:
            self.name = str(name)

        try:
            self.diameter = float(diameter)   # coerce diameter to float
        except ValueError:
            self.diameter = float('nan')

        self.hazardous = bool(hazardous)

        # Creates an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        try:
            fullname = self.designation + " " + self.name
        except TypeError:
            fullname = self.designation
        return fullname

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:     # True = 'is',  False = 'is not'
            haz = 'is'
        else:
            haz = 'is not'
        return f"A NearEarthObject '{self.fullname}' has a diameter of \
        {self.diameter:.3f} km and {haz} hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string."""
        return (f"NearEarthObject(designation={self.designation!r}, \
        name={self.name!r}, "
                f"diameter={self.diameter:.3f}, \
                hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units, and the
    relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time=None, distance=0.0, velocity=0.0,
                    name=None):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to
        the constructor.
        """
        self._designation = str(designation)

        if str(name) == '':   # make sure not empty
            self.name = None
        else:
            self.name = str(name)

        # convert string to datetime object
        self.time = cd_to_datetime(str(time)[:17])
        try:
            self.distance = float(distance)    # coerce to float
        except ValueError:
            self.distance = float('nan')

        try:
            self.velocity = float(velocity)    # coerce to float
        except ValueError:
            self.velocity = float('nan')

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this approach time.

        The value in `self.time` should be a Python `datetime` object. While
        a `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations
        and in serialization to CSV and JSON files.
        """
        time_str = datetime_to_str(self.time)  # datetime to string
        return time_str

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        try:
            fullname = self.designation + " " + self.name
        except TypeError:
            fullname = self.designation
        return fullname

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.fullname}' approaches Earth at \
        a distance of {self.distance:.2f} au and a velocity of \
        {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string."""
        return (f"CloseApproach(_designation={self._designation!r}, \
        time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
