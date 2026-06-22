-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 28, 2025 at 06:13 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medical`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `blood_group` varchar(10) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `preferred_date` date DEFAULT NULL,
  `preferred_time` time DEFAULT NULL,
  `consultation_mode` enum('Physical','Video','Audio') DEFAULT NULL,
  `status` enum('Pending','Accepted','Rejected') DEFAULT 'Pending',
  `shedule` varchar(50) DEFAULT 'Scheduled',
  `video_link` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `patient_id`, `name`, `email`, `phone`, `gender`, `blood_group`, `doctor_id`, `preferred_date`, `preferred_time`, `consultation_mode`, `status`, `shedule`, `video_link`) VALUES
(5, 4, 'Sai', 'Sa@gmail.com', '2222222222', 'Female', 'AB-', 10, '2025-03-28', '15:55:00', 'Physical', 'Pending', 'Scheduled', NULL),
(12, 6, 'ram', 'r@gmail.com', '1234562345', 'Male', 'A+', 10, '2025-04-25', '17:18:00', 'Video', 'Accepted', 'Scheduled', NULL),
(13, 6, 'ram', 'r@gmail.com', '1234562345', 'Male', 'A+', 10, '2025-04-02', '22:54:00', 'Video', 'Accepted', 'Scheduled', NULL),
(15, 7, 'gia', 'g@gmail.com', '2222233333', 'Female', 'A-', 11, '2025-04-08', '13:51:00', 'Video', 'Accepted', 'Rescheduled', NULL),
(37, 11, 'mansi', 'ma@gmail.com', '2222233333', 'Female', 'B+', 10, '2025-04-17', '17:32:00', 'Video', 'Accepted', 'Scheduled', 'https://ecs2.whereby.com/8b7d5731-3bb6-4612-85ad-87a94c148c2c'),
(38, 9, 'kavya', 'k@gmail.com', '9890511217', 'Female', 'A+', 13, '2025-04-12', '22:42:00', 'Video', 'Accepted', 'Rescheduled', 'https://ecs2.whereby.com/5950ba13-277f-433f-bb49-d564a139f524'),
(41, 12, 'p', 'p@gmail.com', '6666699999', 'Female', 'B+', 13, '2025-04-20', '21:40:00', 'Video', 'Accepted', 'Scheduled', 'https://ecs2.whereby.com/88ea5d90-30bf-432c-9969-363ecd69af39'),
(43, 11, 'mansi', 'ma@gmail.com', '2222233333', 'Female', 'B+', 11, '2025-04-24', '19:57:00', 'Physical', 'Pending', 'Scheduled', NULL),
(44, 11, 'mansi', 'ma@gmail.com', '2222233333', 'Female', 'B+', 10, '2025-04-01', '12:10:00', 'Physical', 'Pending', 'Scheduled', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department` varchar(50) NOT NULL,
  `license_no` varchar(6) NOT NULL CHECK (`license_no` regexp '^[0-9]{6}$'),
  `mobile` varchar(10) NOT NULL CHECK (`mobile` regexp '^[0-9]{10}$'),
  `photo` varchar(255) NOT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `active` tinyint(1) DEFAULT 0,
  `password` varchar(255) DEFAULT NULL,
  `education` varchar(255) DEFAULT NULL,
  `certificate` varchar(255) DEFAULT NULL,
  `passing_year` int(11) DEFAULT NULL,
  `experience` int(11) DEFAULT NULL,
  `document` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`id`, `name`, `email`, `department`, `license_no`, `mobile`, `photo`, `status`, `active`, `password`, `education`, `certificate`, `passing_year`, `experience`, `document`) VALUES
(10, 'manali', 'nthorat1011@gmail.com', 'Surgery', '123456', '1111111111', 'img10.jpg', 'approved', 0, 'Manali@29', NULL, NULL, NULL, NULL, NULL),
(11, 'ankita', 'a@gmail.com', 'Cardiology', '898989', '9876543210', 'clock.png', 'approved', 1, 'Manali@29', NULL, NULL, NULL, NULL, NULL),
(13, 'nita', 'n@gmail.com', 'Surgery', '123454', '9890511213', 'img3.jpeg', 'approved', 1, 'Manali@29', 'MBBS', NULL, 1980, 1, 'python_certificate.pdf'),
(16, 'manu', 'm@gmail.com', 'Surgery', '787878', '9890511212', 'clock.png', 'approved', 0, 'Manali@29', 'MBBS', 'dhanu.jpeg', 1991, 2, 'basicsqlcertificate.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_complaint`
--

CREATE TABLE `doctor_complaint` (
  `id` int(11) NOT NULL,
  `complaint` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  `name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_complaint`
--

INSERT INTO `doctor_complaint` (`id`, `complaint`, `submitted_at`, `name`) VALUES
(1, 'sss', '2025-04-18 11:49:24', 'nita'),
(2, 'sss', '2025-04-18 11:49:35', 'nita');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_feedback`
--

CREATE TABLE `doctor_feedback` (
  `id` int(11) NOT NULL,
  `feedback` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  `name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_feedback`
--

INSERT INTO `doctor_feedback` (`id`, `feedback`, `submitted_at`, `name`) VALUES
(1, 'sss', '2025-04-18 12:42:57', 'nita');

-- --------------------------------------------------------

--
-- Table structure for table `druggist`
--

CREATE TABLE `druggist` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `druggist`
--

INSERT INTO `druggist` (`id`, `username`, `password`) VALUES
(1, 'druggist', 'password123');

-- --------------------------------------------------------

--
-- Table structure for table `druggist_complaint`
--

CREATE TABLE `druggist_complaint` (
  `id` int(11) NOT NULL,
  `complaint` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  `name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `druggist_complaint`
--

INSERT INTO `druggist_complaint` (`id`, `complaint`, `submitted_at`, `name`) VALUES
(1, 'mm', '2025-04-18 11:46:44', 'druggist'),
(2, 'fd', '2025-04-18 12:35:07', 'druggist'),
(3, '22', '2025-04-20 11:34:53', 'druggist');

-- --------------------------------------------------------

--
-- Table structure for table `druggist_feedback`
--

CREATE TABLE `druggist_feedback` (
  `id` int(11) NOT NULL,
  `feedback` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  `name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `druggist_feedback`
--

INSERT INTO `druggist_feedback` (`id`, `feedback`, `submitted_at`, `name`) VALUES
(1, 'sss', '2025-04-18 11:46:17', 'druggist'),
(2, 'gdd', '2025-04-21 11:35:44', 'druggist');

-- --------------------------------------------------------

--
-- Table structure for table `emergency_services`
--

CREATE TABLE `emergency_services` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `emergency_services`
--

INSERT INTO `emergency_services` (`id`, `name`, `contact_number`, `image_url`, `address`) VALUES
(2, 's', '1236547891', 'https://media.istockphoto.com/id/1298375809/photo/empty-luxury-modern-hospital-room.webp?a=1&b=1&s=612x612&w=0&k=20&c=IshUd1QTybp-qgJG6FSGk3prbaEqUOjAzbq8GKNWQ98=', 'kharatwadi');

-- --------------------------------------------------------

--
-- Table structure for table `hospital_resources`
--

CREATE TABLE `hospital_resources` (
  `id` int(11) NOT NULL,
  `available_beds` int(11) NOT NULL,
  `ambulance_helpline` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hospital_resources`
--

INSERT INTO `hospital_resources` (`id`, `available_beds`, `ambulance_helpline`) VALUES
(1, 14, '32');

-- --------------------------------------------------------

--
-- Table structure for table `medicines`
--

CREATE TABLE `medicines` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `image` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `medicines`
--

INSERT INTO `medicines` (`id`, `name`, `image`, `price`) VALUES
(1, 'p', '1111.png', 311.00),
(3, 'paracitamin', 'Screenshot_2025-04-01_093650.png', 122.00),
(4, 'fever', 'Screenshot_2023-07-19_211328.png', 200.00),
(5, 'r', 'lotus.jpg', 200.00),
(6, 'Pinu Patil', 'dhanu.jpeg', 22.00),
(7, 'Jivika Sawant ', 'dhanu.jpeg', 22.00),
(8, 'medimix', 'dhanu.jpeg', 12.00);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `address` text NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `birth_date` date NOT NULL,
  `blood_group` enum('A+','A-','B+','B-','O+','O-','AB+','AB-') NOT NULL,
  `image` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`id`, `name`, `email`, `password`, `phone`, `address`, `gender`, `birth_date`, `blood_group`, `image`, `created_at`) VALUES
(4, 'Sai', 'Sa@gmail.com', 'Pass@1234', '2222222222', 'karad', 'Female', '2025-03-05', 'AB-', 'patient_images/patient_4.jpg', '2025-03-27 08:25:01'),
(5, 'nita', 'n@gmail.com', 'Manali@29', '3232323232', 'bahe', 'Female', '2025-03-29', 'B+', 'dhanu.jpeg', '2025-03-27 08:39:18'),
(6, 'ram', 'r@gmail.com', 'Manali@29', '1234562345', 'karad', 'Male', '2025-04-18', 'A+', 'patient_images/patient_6.jpg', '2025-04-01 09:47:37'),
(7, 'gia', 'g@gmail.com', 'Manali@29', '2222233333', 'bahe', 'Female', '2025-04-02', 'A-', 'patient_images/patient_7.jpg', '2025-04-01 10:40:19'),
(8, 'manasi', 'm@gmail.com', 'Manali@29', '2121212121', 'd', 'Female', '2025-04-02', 'A-', 'patient_images/patient_8.jpg', '2025-04-05 05:31:18'),
(9, 'kavya', 'k@gmail.com', 'Manali@29', '9890511217', 'karad', 'Female', '2025-04-08', 'A+', 'nishu.jpg', '2025-04-07 06:41:36'),
(10, 'Jyotsana Sunil Patil', 'j@gmail.com', 'Manali@29', '9696969696', 'karad', 'Female', '2025-04-11', 'A-', 'u2.png', '2025-04-09 07:52:17'),
(11, 'mansi', 'ma@gmail.com', 'Manali@29', '2222233333', 'masur', 'Female', '2025-04-10', 'B+', 'u2.png', '2025-04-09 09:19:20'),
(12, 'p', 'p@gmail.com', 'Manali@29', '6666699999', 'bahe', 'Female', '2025-04-09', 'B+', 'clock.png', '2025-04-11 13:53:37'),
(13, 'divya', 'd@gmail.com', 'Manali@29', '9999966666', 'pp', 'Female', '2025-04-19', 'AB+', 'img10.jpg', '2025-04-17 07:32:31'),
(14, 't', 't@gmail.com', 'Manali@29', '8787878787', 's', 'Male', '2025-04-15', 'A+', 'img3.jpeg', '2025-04-25 08:47:50');

-- --------------------------------------------------------

--
-- Table structure for table `patient_complaint`
--

CREATE TABLE `patient_complaint` (
  `id` int(11) NOT NULL,
  `complaint` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  `name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_complaint`
--

INSERT INTO `patient_complaint` (`id`, `complaint`, `submitted_at`, `name`) VALUES
(1, 'aa', '2025-04-18 11:47:47', NULL),
(2, 'aa', '2025-04-18 11:47:52', NULL),
(3, 'aa', '2025-04-18 11:48:43', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `patient_feedback`
--

CREATE TABLE `patient_feedback` (
  `id` int(11) NOT NULL,
  `feedback` text DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `submitted_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_feedback`
--

INSERT INTO `patient_feedback` (`id`, `feedback`, `name`, `submitted_at`) VALUES
(1, 'll', NULL, '2025-04-18 11:26:44'),
(2, 'ii', NULL, '2025-04-18 11:26:44'),
(3, 'iiii', 'mansi', '2025-04-18 11:26:44'),
(4, 'oo', 'manasi', '2025-04-18 11:26:44'),
(5, 'aas', 'mansi', '2025-04-18 11:26:56'),
(6, 'jj', 'Jyotsana Sunil Patil', '2025-04-18 11:47:35'),
(7, 'nnnn', 'mansi', '2025-04-18 12:06:04'),
(8, 'hh', 'mansi', '2025-04-18 12:14:10');

-- --------------------------------------------------------

--
-- Table structure for table `patient_history`
--

CREATE TABLE `patient_history` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `selected_diseases` text DEFAULT NULL,
  `medicine` varchar(100) DEFAULT NULL,
  `dosage` varchar(100) DEFAULT NULL,
  `doses` int(11) DEFAULT NULL,
  `diet` varchar(100) DEFAULT NULL,
  `diet_plan` text DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `issue_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_history`
--

INSERT INTO `patient_history` (`id`, `patient_id`, `patient_name`, `phone`, `selected_diseases`, `medicine`, `dosage`, `doses`, `diet`, `diet_plan`, `issue_date`, `issue_time`) VALUES
(1, 11, 'mansi', '2222233333', 'Hypertension', 'Amlodipine', '5mg once a day', 1, 'Low Sodium Diet', 'Fruits, vegetables, less salt', '2025-04-28', '20:33:13'),
(2, 11, 'mansi', '2222233333', 'Diabetes', 'Metformin', '500mg twice a day', 2, 'Low Sugar Diet', 'Whole grains, leafy greens, avoid sugar', '2025-04-28', '20:36:22');

-- --------------------------------------------------------

--
-- Table structure for table `prescriptions`
--

CREATE TABLE `prescriptions` (
  `id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prescriptions`
--

INSERT INTO `prescriptions` (`id`, `patient_name`, `filename`, `status`) VALUES
(4, 's', 'prescription_92036.pdf', 'Rejected'),
(5, 'kavya', 'prescription_16050.pdf', 'Active'),
(7, 'mansi', 'prescription_39121.pdf', 'Active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `appointments_ibfk_1` (`patient_id`);

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `license_no` (`license_no`),
  ADD UNIQUE KEY `mobile` (`mobile`);

--
-- Indexes for table `doctor_complaint`
--
ALTER TABLE `doctor_complaint`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctor_feedback`
--
ALTER TABLE `doctor_feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `druggist`
--
ALTER TABLE `druggist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `druggist_complaint`
--
ALTER TABLE `druggist_complaint`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `druggist_feedback`
--
ALTER TABLE `druggist_feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `emergency_services`
--
ALTER TABLE `emergency_services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hospital_resources`
--
ALTER TABLE `hospital_resources`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `medicines`
--
ALTER TABLE `medicines`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `patient_complaint`
--
ALTER TABLE `patient_complaint`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patient_feedback`
--
ALTER TABLE `patient_feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patient_history`
--
ALTER TABLE `patient_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `doctor`
--
ALTER TABLE `doctor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `doctor_complaint`
--
ALTER TABLE `doctor_complaint`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `doctor_feedback`
--
ALTER TABLE `doctor_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `druggist`
--
ALTER TABLE `druggist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `druggist_complaint`
--
ALTER TABLE `druggist_complaint`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `druggist_feedback`
--
ALTER TABLE `druggist_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `emergency_services`
--
ALTER TABLE `emergency_services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `hospital_resources`
--
ALTER TABLE `hospital_resources`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `medicines`
--
ALTER TABLE `medicines`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `patient_complaint`
--
ALTER TABLE `patient_complaint`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `patient_feedback`
--
ALTER TABLE `patient_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `patient_history`
--
ALTER TABLE `patient_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `prescriptions`
--
ALTER TABLE `prescriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
