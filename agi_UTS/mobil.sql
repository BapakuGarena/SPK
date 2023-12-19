-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 30, 2023 at 06:43 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mobil`
--

-- --------------------------------------------------------

--
-- Table structure for table `mobil`
--

CREATE TABLE `mobil` (
  `seri_id` int(5) NOT NULL,
  `nama_mobil` varchar(10) NOT NULL,
  `warna` varchar(11) NOT NULL,
  `harga` int(30) NOT NULL,
  `Jenis` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mobil`
--

INSERT INTO `mobil` (`seri_id`, `nama_mobil`, `warna`, `harga`, `Jenis`) VALUES
(11, 'inova', 'pink', 500000000, 'diesel'),
(12, 'inova', 'merah', 600000000, 'diesel'),
(13, 'fortuner', 'hitam', 700000000, 'diesel'),
(14, 'civic_turb', 'putih', 500000000, 'bensin'),
(15, 'ayla', 'hitam', 200000000, 'bensin'),
(16, 'brio', 'putih', 300000000, 'bensin'),
(17, 'civic_fd', 'silver', 200000000, 'merah'),
(18, 'terios', 'biru', 300000000, 'bensin'),
(19, 'xpander', 'hitam', 300000000, 'bensin'),
(20, 'avanza', 'hitam', 200000000, 'bensin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mobil`
--
ALTER TABLE `mobil`
  ADD PRIMARY KEY (`seri_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mobil`
--
ALTER TABLE `mobil`
  MODIFY `seri_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
