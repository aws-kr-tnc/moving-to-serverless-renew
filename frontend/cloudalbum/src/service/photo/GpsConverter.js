
const gpsConverter = (gpsSource, gpsRef) => {
  let tempArray = '';
  tempArray = gpsSource.toString();
  tempArray = tempArray.split(',');

  let deg = tempArray[0];
  let min = tempArray[1];
  let sec = tempArray[2];
  let ref = gpsRef;

  let dd = parseFloat(deg) + parseFloat(min / 60) + parseFloat(sec / (60 * 60));

  if (ref === 'S' || ref === 'W') {
    dd *= -1;
  } // Don't do anything for N or E

  return dd;
};


export default gpsConverter;
