module.exports = async (req, res) => {
  return res.json({ status: '✅ Vercel respondendo!', time: new Date() });
};