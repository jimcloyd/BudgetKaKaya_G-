const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-4 mt-auto">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm">
          Developed by <span className="font-semibold">Jim Cloyd Estrella</span>
        </p>
        <p className="text-xs text-gray-400 mt-1">
          Family Budget Tracker © {new Date().getFullYear()}
        </p>
      </div>
    </footer>
  )
}

export default Footer
