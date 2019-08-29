const gpsConverter = (gpsSource, gpsRef) => {
  let tempArray;
  tempArray = gpsSource.toString();
  tempArray = tempArray.split(',');

  const deg = parseFloat(tempArray[0]);
  const min = parseFloat(tempArray[1]);
  const sec = parseFloat(tempArray[2]);
  const ref = gpsRef;

  let dd = deg + (min / 60) + (sec / (60 * 60));

  if (ref === 'S' || ref === 'W') {
    dd *= -1;
  } // Don't do anything for N or E

  return dd;
};

export default gpsConverter;
